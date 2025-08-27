import random

# Synonym dictionary for humanizing text
synonyms = {
    "represents": ["shows", "reflects", "signifies", "demonstrates"],
    "multifaceted": ["complex", "many-sided", "layered", "diverse"],
    "psychological": ["mental", "emotional", "cognitive"],
    "phenomenon": ["concept", "idea", "experience", "aspect"],
    "fosters": ["encourages", "promotes", "supports", "nurtures"],
    "social": ["community", "societal", "group-based"],
    "cohesion": ["unity", "togetherness", "bond", "connection"],
    "enhances": ["improves", "boosts", "strengthens", "enriches"],
    "interpersonal": ["human", "relationship-based", "mutual"],
    "well-being": ["happiness", "welfare", "quality of life", "comfort"]
}

def synonym_replace(word):
    """Replace a word with a random synonym if available."""
    if word.lower() in synonyms:
        return random.choice(synonyms[word.lower()])
    return word

def restructure_sentence(text):
    """Restructure sentence for more human-like variation."""
    if "represents" in text:
        text = text.replace("represents", "can be seen as")
    if "that" in text:
        text = text.replace("that", "which often")
    return text

def humanize_text(text):
    """Main function to humanize AI text."""
    words = text.split()
    new_words = [synonym_replace(word) for word in words]
    humanized = " ".join(new_words)

    # Apply sentence restructuring
    humanized = restructure_sentence(humanized)

    # Add a natural human-like touch at the end
    extras = [
        "In simple terms, it's what brings people closer.",
        "At its core, it’s about connection and care.",
        "That’s why it feels so essential in our lives.",
        "In the end, love is what keeps relationships alive."
    ]
    if random.random() > 0.5:  # Add extra sentence half the time
        humanized += " " + random.choice(extras)

    return humanized
