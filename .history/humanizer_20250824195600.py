import random

def humanize_paragraph(text: str) -> str:
    # Split into sentences
    sentences = text.split(". ")
    
    # Shuffle some sentences to reduce AI similarity
    random.shuffle(sentences)
    
    # Add slight variations
    variations = [
        lambda s: s.replace("technology", "tech"),
        lambda s: s.replace("Artificial Intelligence", "AI"),
        lambda s: s.replace("crucial", "important"),
        lambda s: s.replace("transforming", "reshaping"),
    ]
    
    new_sentences = []
    for s in sentences:
        if random.random() < 0.4:  # randomly apply variation
            s = random.choice(variations)(s)
        new_sentences.append(s)
    
    return ". ".join(new_sentences)
