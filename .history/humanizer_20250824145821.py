from transformers import pipeline
import random
import re

# Load a stronger paraphrasing model
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def clean_output(text: str) -> str:
    """Cleans unnecessary spaces and fixes casing."""
    text = re.sub(r"\s+", " ", text).strip()
    if text and not text.endswith("."):
        text += "."
    return text[0].upper() + text[1:] if text else text

def humanize_text(text: str) -> str:
    """
    Takes AI-generated text and rewrites it into a more natural, human-like version.
    Uses sampling, multiple generations, and light randomization.
    """
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate multiple paraphrased outputs
        outputs = paraphraser(
            text,
            max_length=256,
            num_return_sequences=5,   # get 5 variations
            do_sample=True,           
            temperature=1.1,          # slightly higher creativity
            top_p=0.92,               
            top_k=60                  
        )

        # Collect unique candidates
        candidates = list({clean_output(o["generated_text"]) for o in outputs if "generated_text" in o})

        # If model gives too similar results → shuffle manually
        if not candidates:
            return text  # fallback

        # Strategy to choose:
        # - Sometimes longest sentence
        # - Sometimes random for diversity
        if random.random() > 0.4:
            humanized = max(candidates, key=len)
        else:
            humanized = random.choice(candidates)

        return humanized

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"


# Example run
if __name__ == "__main__":
    sample = "AI-generated content often feels repetitive and unnatural, but it can be improved through better rewriting."
    print("Original:", sample)
    print("Humanized:", humanize_text(sample))
