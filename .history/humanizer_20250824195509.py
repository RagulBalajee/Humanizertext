# humanizer.py
import random
from difflib import SequenceMatcher

# Basic synonym map (can be expanded)
synonyms = {
    "rapidly": ["quickly", "swiftly"],
    "transforming": ["revolutionizing", "changing"],
    "industries": ["sectors", "fields"],
    "enabling": ["allowing", "empowering"],
    "perform": ["carry out", "do"],
    "tasks": ["jobs", "responsibilities"],
    "intelligence": ["reasoning", "smartness"],
    "reshaping": ["altering", "revolutionizing"],
    "analyze": ["process", "examine"],
    "vast": ["huge", "large"],
    "amounts": ["volumes", "quantities"],
    "concerns": ["worries", "challenges"],
    "responsible": ["ethical", "accountable"],
    "balance": ["equilibrium", "middle ground"],
    "innovation": ["progress", "advancement"],
    "ethics": ["morality", "fairness"],
    "crucial": ["essential", "vital"],
}

def replace_synonyms(sentence: str) -> str:
    words = sentence.split()
    new_words = []
    for word in words:
        key = word.lower().strip(".,")
        if key in synonyms and random.random() < 0.4:  # 40% chance to replace
            new_words.append(random.choice(synonyms[key]))
        else:
            new_words.append(word)
    return " ".join(new_words)

def humanize_text(text: str) -> str:
    sentences = text.split(". ")
    # Shuffle sentence order a bit
    random.shuffle(sentences)
    rewritten = []
    for sentence in sentences:
        rewritten.append(replace_synonyms(sentence))
    return ". ".join(rewritten)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
    original = """Artificial Intelligence (AI) is rapidly transforming industries by enabling machines to perform tasks that once required human intelligence. From natural language processing and image recognition to autonomous vehicles and medical diagnostics, AI is reshaping how businesses operate and how people interact with technology. Its ability to analyze vast amounts of data and learn patterns allows organizations to make smarter decisions and create personalized experiences. However, concerns about job displacement, data privacy, and algorithmic bias highlight the need for responsible AI development. Striking a balance between innovation and ethics will be crucial to ensuring AI benefits society as a whole."""

    humanized = humanize_text(original)

    print("\n--- Original Paragraph ---\n")
    print(original)
    print("\n--- Humanized Paragraph ---\n")
    print(humanized)
    print("\n--- Similarity Score ---")
    print(f"{similarity(original, humanized) * 100:.2f}%")
