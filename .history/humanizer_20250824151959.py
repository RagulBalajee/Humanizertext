import random

class Humanizer:
    def __init__(self):
        # Some transformation patterns for variation
        self.synonyms = {
            "important": ["crucial", "vital", "significant", "essential"],
            "powerful": ["influential", "impactful", "strong", "dominant"],
            "love": ["affection", "compassion", "care", "devotion"],
            "society": ["community", "civilization", "people", "humanity"],
            "technology": ["innovation", "digital tools", "modern tech", "advancement"],
            "future": ["tomorrow", "coming years", "next era", "ahead"]
        }

    def replace_synonyms(self, text: str) -> str:
        """Replace words with random synonyms for variation"""
        words = text.split()
        new_words = []
        for word in words:
            lw = word.lower().strip(".,!?")
            if lw in self.synonyms:
                new_words.append(random.choice(self.synonyms[lw]))
            else:
                new_words.append(word)
        return " ".join(new_words)

    def restructure_sentence(self, text: str) -> str:
        """Add small restructuring for variety"""
        sentences = text.split(". ")
        new_sentences = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            if random.random() > 0.5:
                new_sentences.append(s)
            else:
                new_sentences.append(f"In essence, {s[0].lower() + s[1:]}")
        return ". ".join(new_sentences)

    def humanize(self, text: str) -> str:
        """Apply synonym replacement + restructuring"""
        step1 = self.replace_synonyms(text)
        step2 = self.restructure_sentence(step1)
        return step2
