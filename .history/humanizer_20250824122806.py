from transformers import pipeline

# Load a paraphrasing model (small + effective for humanizing AI text)
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def humanize_text(text: str) -> str:
    """
    Takes AI-generated text and rewrites it into a more human-like version.
    """
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate a paraphrased version
        outputs = paraphraser(
            text,
            max_length=256,
            num_return_sequences=1,
            temperature=0.8,   # adds variation
            top_p=0.9          # sampling for diversity
        )

        return outputs[0]["generated_text"]

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"
