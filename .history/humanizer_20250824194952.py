import random
import re  

# Synonym mapping (expand as needed)
synonyms = {
    "students": ["learners", "pupils"],
    "teachers": ["educators", "instructors"],
    "technology": ["tech", "digital tools"],
    "education": ["learning", "schooling"],
    "important": ["crucial", "vital", "significant"],
    "future": ["next era", "coming years"],
    "resources": ["materials", "content"],
    "interactive": ["engaging", "hands-on"],
    "skills": ["abilities", "capabilities"],
    "global": ["worldwide", "across the planet"],
    "barriers": ["obstacles", "gaps"]
}

def humanize_sentence(sentence: str) -> str:
    words = sentence.split()
    new_words = []

    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        if clean_word in synonyms and random.random() < 0.6:  # 60% chance to replace
            new_words.append(random.choice(synonyms[clean_word]))
        else:
            new_words.append(word)

    # Restructure by sometimes shuffling parts
    if len(new_words) > 8 and random.random() < 0.4:
        split_point = len(new_words) // 2
        new_words = new_words[split_point:] + new_words[:split_point]

    return " ".join(new_words)

def humanize_paragraph(paragraph: str) -> str:
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    new_sentences = []

    for s in sentences:
        if s.strip():
            new_sentences.append(humanize_sentence(s))

    # Reorder sentences randomly
    random.shuffle(new_sentences)

    return " ".join(new_sentences)
