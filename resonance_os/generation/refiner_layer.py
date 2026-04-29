class RefinerLayer:
    def refine(self, sentence: str, hrv_feedback: float) -> str:
        # Adjust sentence to improve HRV resonance
        return sentence + f" [Refined with HRV feedback {hrv_feedback:.2f}]"
