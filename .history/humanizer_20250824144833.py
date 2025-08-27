from transformers import pipeline
import random

# Load a stronger paraphrasing model
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def humanize_text(text: str) -> str:
    """
    Takes AI-generated text and rewrites it into a more natural, human-like version.
    Uses sampling and multiple generations to improve diversity.
    """
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate multiple paraphrased outputs
        outputs = paraphraser(
            text,
            max_length=256,
            num_return_sequences=3,   # get 3 variations
            do_sample=True,           # randomness ON
            temperature=1.0,          # creativity
            top_p=0.92,               # nucleus sampling
            top_k=50                  # limits word choices for diversity
        )

        # Clean the outputs
        candidates = [o["generated_text"].strip() for o in outputs if "generated_text" in o]

        # Pick one candidate:
        # strategy → choose the longest one (tends to be more human-like)
        humanized = max(candidates, key=len) if candidates else text

        return humanized

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"


# Example run
if __name__ == "__main__":
    sample = "AI-generated content often feels repetitive and unnatural, but it can be improved through better rewriting."
    print("Original:", sample)
    print("Humanized:", humanize_text(sample))
