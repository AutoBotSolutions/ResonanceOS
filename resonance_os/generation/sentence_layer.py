class SentenceLayer:
    def generate_sentences(self, outline: str, target_hrv):
        # Generate sentences constrained by target HRV vector
        sentences = [
            f"Sentence with target valence {target_hrv[1]:.2f} from outline: {outline}"
        ]
        return sentences
