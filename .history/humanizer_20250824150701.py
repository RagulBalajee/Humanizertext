import random
import re

# Synonym dictionary for paraphrasing
synonym_map = {
    "modern": ["contemporary", "current", "present-day"],
    "digital": ["online", "virtual", "tech-driven"],
    "economy": ["market", "industry", "business landscape"],
    "critical": ["essential", "vital", "fundamental"],
    "driver": ["force", "catalyst", "engine"],
    "efficiency": ["productivity", "performance", "effectiveness"],
    "organizations": ["companies", "businesses", "enterprises"],
    "process": ["handle", "analyze", "manage"],
    "vast": ["large-scale", "huge", "extensive"],
    "datasets": ["data collections", "information pools", "records"],
    "optimize": ["streamline", "enhance", "improve"],
    "operations": ["workflows", "processes", "functions"],
    "unlock": ["unleash", "enable", "open up"],
    "innovative": ["creative", "groundbreaking", "novel"],
    "solutions": ["approaches", "methods", "strategies"],
    "redefine": ["transform", "reshape", "revolutionize"],
    "standards": ["norms", "benchmarks", "expectations"],
}

def synonym_replace(text: str) -> str:
    """Replace words with synonyms to humanize text."""
    words = text.split()
    new_words = []
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word).lower()  # strip punctuation
        if clean_word in synonym_map and random.random() < 0.6:  # 60% chance of replacement
            new_word = random.choice(synonym_map[clean_word])
            # Preserve capitalization
            if word[0].isupper():
                new_word = new_word.capitalize()
            # Keep punctuation
            if word[-1] in ",.!?":
                new_word += word[-1]
            new_words.append(new_word)
        else:
            new_words.append(word)
    return " ".join(new_words)

def restructure_sentences(text: str) -> str:
    """Restructure sentence for variation."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    random.shuffle(sentences)
    return " ".join(sentences)

def humanize_text(ai_text: str) -> str:
    """Main function to humanize AI text."""
    # Step 1: Synonym replacement
    step1 = synonym_replace(ai_text)

    # Step 2: Random sentence restructuring
    step2 = restructure_sentences(step1)

    # Step 3: Slight punctuation/style variation
    step3 = step2.replace(" ,", ",").replace(" .", ".")
    if random.random() > 0.5:
        step3 = step3.replace(" and ", ", as well as ")

    return step3
