from transformers import pipeline
import random

# Load a paraphrasing model (T5 small / Pegasus can also be used)
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def humanize_text(text, tone="casual"):
    # Step 1: Paraphrase the text
    paraphrases = paraphraser(
        f"paraphrase: {text}", 
        max_length=200, 
        num_return_sequences=5, 
        do_sample=True
    )

    # Step 2: Pick a random paraphrase
    result = random.choice(paraphrases)['generated_text']

    # Step 3: Add human-like connectors and tone adjustments
    connectors = {
        "casual": ["Honestly,", "You know,", "Well,", "To be real,"],
        "formal": ["In fact,", "Notably,", "Furthermore,", "Interestingly,"],
        "storytelling": ["Once upon a time,", "Back in the day,", "Surprisingly,"]
    }

    if random.random() > 0.5:
        result = random.choice(connectors.get(tone, [])) + " " + result

    return result
