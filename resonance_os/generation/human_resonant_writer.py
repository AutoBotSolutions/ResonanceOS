from .planner_layer import PlannerLayer
from .sentence_layer import SentenceLayer
from .refiner_layer import RefinerLayer
from .hrf_model import HRFModel

class HumanResonantWriter:
    def __init__(self):
        self.planner = PlannerLayer()
        self.sentence_layer = SentenceLayer()
        self.refiner = RefinerLayer()
        self.hrf = HRFModel()

    def generate(self, prompt: str):
        article = ""
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        for outline, hrv_target in zip(paragraphs, target_hrvs):
            sentences = self.sentence_layer.generate_sentences(outline, hrv_target)
            for s in sentences:
                feedback = self.hrf.predict(s)
                refined = self.refiner.refine(s, feedback)
                article += refined + " "
        return article
