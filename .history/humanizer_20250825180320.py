# humanizer.py
import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

# Make sure punkt is downloaded
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

def synonym_replace(word):
    """Replace a word with a synonym if available"""
    synonyms = wordnet.synsets(word)
    if not synonyms:
        return word
    words = set()
    for syn in synonyms:
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                words.add(lemma.name().replace("_", " "))
    return random.choice(list(words)) if words else word

def humanize_paragraph(text: str) -> str:
    """Takes AI-generated text and makes it sound more human"""
    
    # Step 1: Break text into sentences
    sentences = sent_tokenize(text)

    # Step 2: Randomly shuffle a few sentences (not all, keeps coherence)
    if len(sentences) > 2:
        random.shuffle(sentences)

    new_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        new_words = []

        for word in words:
            # Randomly replace some words with synonyms
            if word.isalpha() and random.random() < 0.2:  
                new_words.append(synonym_replace(word))
            else:
                new_words.append(word)

        # Randomly drop/add filler words for human-like effect
        if random.random() < 0.3:
            fillers = ["actually", "basically", "to be honest", "in fact", "overall"]
            new_words.insert(0, random.choice(fillers))

        new_sent = " ".join(new_words)
        new_sentences.append(new_sent)

    # Step 3: Return as final "humanized" paragraph
    return " ".join(new_sentences)
