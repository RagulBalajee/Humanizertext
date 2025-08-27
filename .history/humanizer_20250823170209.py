from transformers import pipeline
import random

# Load a pre-trained paraphrasing model
# First time it may take time to download the model
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def humanize_text(text: str, tone: str = "casual") -> str:
    """
    Takes AI-generated text and returns a humanized version.
    Supports tone adjustment: casual, formal, storytelling.
    """

    if not text.strip():
        return "⚠️ Empty input provided. Please enter some text."

    # Step 1: Generate multiple paraphrases
    paraphrases = paraphraser(
        f"paraphrase: {text}",
        max_length=200,
        num_return_sequences=5,
        do_sample=True
    )

    # Step 2: Pick one paraphrased version randomly
    result = random.choice(paraphrases)["generated_text"]

    # Step 3: Add natural connectors depending on tone
    connectors = {
        "casual": ["Honestly,", "You know,", "Well,", "To be real,"],
        "formal": ["In fact,", "Notably,", "Furthermore,", "Interestingly,"],
        "storytelling": ["Once upon a time,", "Back in the day,", "Surprisingly,"]
    }

    if random.random() > 0.5 and tone in connectors:
        result = random.choice(connectors[tone]) + " " + result

    return result
