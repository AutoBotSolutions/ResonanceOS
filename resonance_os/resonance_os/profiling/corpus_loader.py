"""
Corpus loading and preprocessing for ResonanceOS
"""

import os
import json
import chardet
from pathlib import Path
from typing import List, Dict, Iterator, Optional, Union
from dataclasses import dataclass
import re

from ..core.types import CorpusInfo
from ..core.logging import get_logger, log_performance
from ..core.config import get_config

logger = get_logger(__name__)


@dataclass
class TextDocument:
    """Single text document"""
    content: str
    source: str
    file_path: Optional[Path] = None
    metadata: Optional[Dict] = None


class CorpusLoader:
    """Loads and processes text corpora for style analysis"""
    
    def __init__(self):
        self.config = get_config()
        self.supported_extensions = {'.txt', '.md', '.rtf', '.html', '.htm'}
    
    @log_performance
    def load_corpus(
        self,
        path: Union[str, Path],
        recursive: bool = True,
        encoding: Optional[str] = None
    ) -> List[TextDocument]:
        """Load corpus from directory or file"""
        
        path = Path(path)
        documents = []
        
        if path.is_file():
            documents.extend(self._load_file(path, encoding))
        elif path.is_dir():
            documents.extend(self._load_directory(path, recursive, encoding))
        else:
            raise FileNotFoundError(f"Path not found: {path}")
        
        logger.info(f"Loaded {len(documents)} documents from {path}")
        return documents
    
    def _load_directory(
        self,
        directory: Path,
        recursive: bool,
        encoding: Optional[str]
    ) -> List[TextDocument]:
        """Load all supported files from directory"""
        
        documents = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    docs = self._load_file(file_path, encoding)
                    documents.extend(docs)
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {str(e)}")
        
        return documents
    
    def _load_file(
        self,
        file_path: Path,
        encoding: Optional[str]
    ) -> List[TextDocument]:
        """Load single file and split into documents"""
        
        # Detect encoding if not specified
        if encoding is None:
            encoding = self._detect_encoding(file_path)
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Clean and preprocess content
            content = self._preprocess_content(content)
            
            # Split into chunks if very long
            if len(content) > 10000:  # Split long documents
                chunks = self._split_content(content, file_path)
                return chunks
            else:
                return [TextDocument(
                    content=content,
                    source=str(file_path),
                    file_path=file_path,
                    metadata={'encoding': encoding}
                )]
        
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in {file_path}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            return []
    
    def _detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')
                confidence = result.get('confidence', 0.0)
                
                if confidence < 0.7:
                    logger.warning(f"Low encoding confidence ({confidence:.2f}) for {file_path}")
                
                return encoding or 'utf-8'
        except Exception:
            return 'utf-8'
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess text content"""
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove HTML tags if present
        content = re.sub(r'<[^>]+>', ' ', content)
        
        # Normalize quotes
        content = re.sub(r'[""''`]', '"', content)
        
        # Remove excessive punctuation
        content = re.sub(r'[!]{3,}', '!', content)
        content = re.sub(r'[?]{3,}', '?', content)
        content = re.sub(r'[.]{3,}', '...', content)
        
        # Fix spacing around punctuation
        content = re.sub(r'\s+([,.!?;:])', r'\1', content)
        content = re.sub(r'([,.!?;:])\s+', r'\1 ', content)
        
        return content.strip()
    
    def _split_content(self, content: str, source_path: Path) -> List[TextDocument]:
        """Split long content into smaller chunks"""
        
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 <= 5000:  # Max chunk size
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Create documents from chunks
        documents = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 100:  # Minimum chunk size
                documents.append(TextDocument(
                    content=chunk.strip(),
                    source=f"{source_path}_chunk_{i+1}",
                    file_path=source_path,
                    metadata={'chunk_index': i, 'total_chunks': len(chunks)}
                ))
        
        return documents
    
    @log_performance
    def analyze_corpus(self, documents: List[TextDocument]) -> CorpusInfo:
        """Analyze corpus statistics"""
        
        if not documents:
            raise ValueError("No documents to analyze")
        
        total_chars = sum(len(doc.content) for doc in documents)
        total_words = sum(len(doc.content.split()) for doc in documents)
        total_sentences = sum(len(re.findall(r'[.!?]+', doc.content)) for doc in documents)
        
        avg_sentence_length = total_words / max(total_sentences, 1)
        
        # Detect language (simplified)
        sample_text = " ".join(doc.content[:500] for doc in documents[:3])
        language = self._detect_language(sample_text)
        
        return CorpusInfo(
            name=f"Corpus_{len(documents)}_docs",
            source="loaded_files",
            file_count=len(documents),
            total_characters=total_chars,
            total_words=total_words,
            total_sentences=total_sentences,
            avg_sentence_length=avg_sentence_length,
            language=language
        )
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on common words"""
        
        # Very basic detection - could be enhanced with proper language detection
        common_english = ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with']
        words = text.lower().split()
        
        if words:
            english_ratio = sum(1 for word in words[:100] if word in common_english) / min(len(words), 100)
            return 'en' if english_ratio > 0.1 else 'unknown'
        
        return 'unknown'
    
    def save_corpus_info(self, info: CorpusInfo, output_path: Path):
        """Save corpus analysis to file"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(info.dict(), f, indent=2, default=str)
        
        logger.info(f"Saved corpus info to {output_path}")
    
    def load_corpus_info(self, input_path: Path) -> CorpusInfo:
        """Load corpus analysis from file"""
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return CorpusInfo(**data)


class DocumentIterator:
    """Iterator for large corpora to avoid memory issues"""
    
    def __init__(self, corpus_path: Path, batch_size: int = 100):
        self.corpus_path = corpus_path
        self.batch_size = batch_size
        self.loader = CorpusLoader()
        self.file_paths = self._get_file_paths()
        self.current_index = 0
    
    def _get_file_paths(self) -> List[Path]:
        """Get all supported file paths"""
        paths = []
        for file_path in self.corpus_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.loader.supported_extensions:
                paths.append(file_path)
        return paths
    
    def __iter__(self):
        self.current_index = 0
        return self
    
    def __next__(self) -> List[TextDocument]:
        """Get next batch of documents"""
        
        if self.current_index >= len(self.file_paths):
            raise StopIteration
        
        batch_paths = self.file_paths[self.current_index:self.current_index + self.batch_size]
        documents = []
        
        for file_path in batch_paths:
            try:
                docs = self.loader._load_file(file_path, None)
                documents.extend(docs)
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {str(e)}")
        
        self.current_index += self.batch_size
        return documents
    
    def __len__(self) -> int:
        """Number of batches"""
        return (len(self.file_paths) + self.batch_size - 1) // self.batch_size
