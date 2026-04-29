"""
Profile persistence for ResonanceOS
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np

from ..core.types import StyleProfile, ResonanceVector
from ..core.logging import get_logger, log_performance
from ..core.config import get_config

logger = get_logger(__name__)


class ProfilePersistence:
    """Handles saving and loading of style profiles"""
    
    def __init__(self, profiles_dir: Optional[Path] = None):
        self.config = get_config()
        self.profiles_dir = profiles_dir or self.config.paths.profiles_dir
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    @log_performance
    def save_profile(self, profile: StyleProfile, format: str = "json") -> Path:
        """Save style profile to disk"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{profile.name}_{timestamp}.{format}"
        file_path = self.profiles_dir / filename
        
        if format.lower() == "json":
            self._save_json(profile, file_path)
        elif format.lower() == "pickle":
            self._save_pickle(profile, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Saved profile '{profile.name}' to {file_path}")
        return file_path
    
    def _save_json(self, profile: StyleProfile, file_path: Path):
        """Save profile as JSON"""
        
        # Convert to dict and handle numpy arrays
        profile_dict = profile.dict()
        
        # Add metadata
        profile_dict['saved_at'] = datetime.now().isoformat()
        profile_dict['format_version'] = "1.0"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profile_dict, f, indent=2, default=str)
    
    def _save_pickle(self, profile: StyleProfile, file_path: Path):
        """Save profile as pickle"""
        
        with open(file_path, 'wb') as f:
            pickle.dump(profile, f)
    
    @log_performance
    def load_profile(self, file_path: Path, format: Optional[str] = None) -> StyleProfile:
        """Load style profile from disk"""
        
        if format is None:
            format = file_path.suffix.lstrip('.')
        
        if format.lower() == "json":
            return self._load_json(file_path)
        elif format.lower() == "pickle":
            return self._load_pickle(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _load_json(self, file_path: Path) -> StyleProfile:
        """Load profile from JSON"""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle legacy formats
        if 'resonance_vector' in data and isinstance(data['resonance_vector'], dict):
            # New format with full ResonanceVector
            return StyleProfile(**data)
        elif 'resonance_vector' in data and isinstance(data['resonance_vector'], list):
            # Legacy format with just vector values
            data['resonance_vector'] = ResonanceVector(
                values=data['resonance_vector'],
                dimensions=self._get_default_dimensions(),
                confidence=1.0
            )
            return StyleProfile(**data)
        else:
            raise ValueError("Invalid profile format")
    
    def _load_pickle(self, file_path: Path) -> StyleProfile:
        """Load profile from pickle"""
        
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    def _get_default_dimensions(self) -> List[str]:
        """Get default resonance dimensions"""
        from ..core.constants import RESONANCE_DIMENSIONS
        return RESONANCE_DIMENSIONS
    
    @log_performance
    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all available profiles"""
        
        profiles = []
        
        for file_path in self.profiles_dir.glob("*.json"):
            try:
                profile_info = self._get_profile_info(file_path, "json")
                profiles.append(profile_info)
            except Exception as e:
                logger.warning(f"Failed to read profile info from {file_path}: {str(e)}")
        
        for file_path in self.profiles_dir.glob("*.pickle"):
            try:
                profile_info = self._get_profile_info(file_path, "pickle")
                profiles.append(profile_info)
            except Exception as e:
                logger.warning(f"Failed to read profile info from {file_path}: {str(e)}")
        
        # Sort by creation date
        profiles.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return profiles
    
    def _get_profile_info(self, file_path: Path, format: str) -> Dict[str, Any]:
        """Get basic profile information without loading full data"""
        
        if format == "json":
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'name': data.get('name', file_path.stem),
                'description': data.get('description'),
                'file_path': str(file_path),
                'format': format,
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'confidence': data.get('resonance_vector', {}).get('confidence', 0.0),
                'metadata': data.get('metadata', {})
            }
        
        elif format == "pickle":
            # For pickle files, we need to load the full profile
            profile = self._load_pickle(file_path)
            return {
                'name': profile.name,
                'description': profile.description,
                'file_path': str(file_path),
                'format': format,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at,
                'confidence': profile.resonance_vector.confidence,
                'metadata': profile.metadata
            }
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def load_profile_by_name(self, name: str) -> Optional[StyleProfile]:
        """Load profile by name (finds most recent version)"""
        
        profiles = self.list_profiles()
        
        for profile_info in profiles:
            if profile_info['name'] == name:
                file_path = Path(profile_info['file_path'])
                return self.load_profile(file_path)
        
        return None
    
    def delete_profile(self, name: str) -> bool:
        """Delete all versions of a profile"""
        
        deleted = False
        profiles = self.list_profiles()
        
        for profile_info in profiles:
            if profile_info['name'] == name:
                file_path = Path(profile_info['file_path'])
                try:
                    file_path.unlink()
                    deleted = True
                    logger.info(f"Deleted profile file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {str(e)}")
        
        return deleted
    
    def export_profiles(self, output_path: Path, profile_names: Optional[List[str]] = None):
        """Export profiles to a single file"""
        
        profiles_to_export = []
        
        if profile_names:
            # Export specific profiles
            for name in profile_names:
                profile = self.load_profile_by_name(name)
                if profile:
                    profiles_to_export.append(profile)
                else:
                    logger.warning(f"Profile not found: {name}")
        else:
            # Export all profiles
            profiles = self.list_profiles()
            for profile_info in profiles:
                profile = self.load_profile(Path(profile_info['file_path']))
                profiles_to_export.append(profile)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0',
            'profiles': [profile.dict() for profile in profiles_to_export]
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Exported {len(profiles_to_export)} profiles to {output_path}")
    
    def import_profiles(self, input_path: Path) -> int:
        """Import profiles from export file"""
        
        with open(input_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        imported_count = 0
        
        for profile_dict in import_data.get('profiles', []):
            try:
                profile = StyleProfile(**profile_dict)
                self.save_profile(profile)
                imported_count += 1
            except Exception as e:
                logger.error(f"Failed to import profile {profile_dict.get('name', 'unknown')}: {str(e)}")
        
        logger.info(f"Imported {imported_count} profiles from {input_path}")
        return imported_count
    
    def create_profile_backup(self) -> Path:
        """Create backup of all profiles"""
        
        backup_dir = self.profiles_dir.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"profiles_backup_{timestamp}.json"
        
        self.export_profiles(backup_path)
        
        logger.info(f"Created profile backup: {backup_path}")
        return backup_path
    
    def restore_profile_backup(self, backup_path: Path) -> int:
        """Restore profiles from backup"""
        
        return self.import_profiles(backup_path)
    
    def validate_profile(self, profile: StyleProfile) -> List[str]:
        """Validate profile structure and data"""
        
        errors = []
        
        # Check required fields
        if not profile.name:
            errors.append("Profile name is required")
        
        if not profile.resonance_vector:
            errors.append("Resonance vector is required")
        
        # Check resonance vector
        if profile.resonance_vector:
            if not profile.resonance_vector.values:
                errors.append("Resonance vector values are required")
            
            if not profile.resonance_vector.dimensions:
                errors.append("Resonance vector dimensions are required")
            
            if len(profile.resonance_vector.values) != len(profile.resonance_vector.dimensions):
                errors.append("Resonance vector values and dimensions must have same length")
            
            # Check value ranges
            for i, value in enumerate(profile.resonance_vector.values):
                if not isinstance(value, (int, float)):
                    errors.append(f"Resonance vector value {i} must be numeric")
                elif value < 0 or value > 1:
                    errors.append(f"Resonance vector value {i} must be between 0 and 1")
        
        # Check emotional curve
        if profile.emotional_curve:
            for i, value in enumerate(profile.emotional_curve):
                if not isinstance(value, (int, float)):
                    errors.append(f"Emotional curve value {i} must be numeric")
                elif value < 0 or value > 1:
                    errors.append(f"Emotional curve value {i} must be between 0 and 1")
        
        # Check cadence pattern
        if profile.cadence_pattern:
            for i, value in enumerate(profile.cadence_pattern):
                if not isinstance(value, (int, float)):
                    errors.append(f"Cadence pattern value {i} must be numeric")
                elif value < 0 or value > 1:
                    errors.append(f"Cadence pattern value {i} must be between 0 and 1")
        
        # Check abstraction preference
        if not isinstance(profile.abstraction_preference, (int, float)):
            errors.append("Abstraction preference must be numeric")
        elif profile.abstraction_preference < 0 or profile.abstraction_preference > 1:
            errors.append("Abstraction preference must be between 0 and 1")
        
        return errors
    
    def get_profile_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored profiles"""
        
        profiles = self.list_profiles()
        
        if not profiles:
            return {
                'total_profiles': 0,
                'average_confidence': 0.0,
                'oldest_profile': None,
                'newest_profile': None,
                'formats': {}
            }
        
        confidences = [p.get('confidence', 0.0) for p in profiles]
        formats = {}
        
        for profile in profiles:
            format_type = profile.get('format', 'unknown')
            formats[format_type] = formats.get(format_type, 0) + 1
        
        return {
            'total_profiles': len(profiles),
            'average_confidence': sum(confidences) / len(confidences),
            'oldest_profile': min(profiles, key=lambda x: x.get('created_at', ''))['name'],
            'newest_profile': max(profiles, key=lambda x: x.get('created_at', ''))['name'],
            'formats': formats
        }
