import random

class Humanizer:
    def __init__(self):
        # Different transformation strategies
        self.strategies = [
            self.expand_meaning,
            self.restructure_sentence,
            self.casual_tone,
            self.formal_tone,
            self.add_emotion
        ]

    def humanize(self, text: str, num_variations: int = 3) -> list:
        """Generate multiple human-like variations of a given text."""
        variations = set()
        while len(variations) < num_variations:
            strategy = random.choice(self.strategies)
            variations.add(strategy(text))
        return list(variations)

    def expand_meaning(self, text: str) -> str:
        return text + " It not only informs but also connects people in ways that shape shared experiences."

    def restructure_sentence(self, text: str) -> str:
        return "At its core, " + text.lower().replace("is", "serves as")

    def casual_tone(self, text: str) -> str:
        return "You know, " + text.replace("is", "can be") + " — something we all relate to in everyday life."

    def formal_tone(self, text: str) -> str:
        return "In a broader perspective, " + text.replace("is", "functions as") + " within modern society."

    def add_emotion(self, text: str) -> str:
        return text + " It inspires feelings, sparks imagination, and often leaves lasting memories."
