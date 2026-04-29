import random
from typing import List, Tuple

class PlannerLayer:
    def plan_paragraphs(self, prompt: str, num_paragraphs=3) -> Tuple[List[str], List[List[float]]]:
        # Generate paragraph-level outlines and target HRV vectors
        paragraphs = [f"Paragraph outline {i+1} for: {prompt}" for i in range(num_paragraphs)]
        target_hrvs = [[random.random() for _ in range(8)] for _ in range(num_paragraphs)]  # placeholder HRVs
        return paragraphs, target_hrvs
