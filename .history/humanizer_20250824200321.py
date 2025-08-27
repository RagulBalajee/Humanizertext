# humanizer.py
from transformers import pipeline
import random
import nltk
from nltk.corpus import wordnet
import re

nltk.download('wordnet')
nltk.download('omw-1.4')

# Load a stronger paraphrasing model
paraphraser = pipeline("text2text-generation", model="ramsrigouthamg/t5_paraphraser", device=-1)

def replace_synonyms(sentence):
    """Replace some words with synonyms to increase variation."""
    words = sentence.split()
    new_words = []
    for word in words:
        if random.random() < 0.15:  # 15% chance to replace a word
            syns = wordnet.synsets(word)
            if syns:
                lemmas = [l.name().replace('_', ' ') for l in syns[0].lemmas()]
                if lemmas:
                    new_word = random.choice(lemmas)
                    new_words.append(new_word)
                    continue
        new_words.append(word)
    return ' '.join(new_words)

def reorder_sentences(paragraph):
    """Randomly shuffle sentences slightly to create variation."""
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    random.shuffle(sentences)
    return ' '.join(sentences)

def humanize_paragraph(text: str) -> str:
    """Generate a humanized version of AI-generated paragraph."""
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate multiple paraphrased outputs
        outputs = paraphraser(
            text,
            max_length=512,
            num_return_sequences=5,
            do_sample=True,
            temperature=0.9,
            top_p=0.9
        )

        # Clean outputs
        candidates = [o["generated_text"].strip() for o in outputs if "generated_text" in o]

        # Pick one candidate randomly
        humanized = random.choice(candidates)

        # Post-process: reorder sentences
        humanized = reorder_sentences(humanized)

        # Post-process: replace some words with synonyms
        humanized = replace_synonyms(humanized)

        return humanized

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"
