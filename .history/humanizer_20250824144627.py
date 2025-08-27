from transformers import pipeline

# Load a paraphrasing model (T5 fine-tuned on PAWS dataset)
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def humanize_text(text: str) -> str:
    """
    Takes AI-generated text and rewrites it into a more human-like version.
    """
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate a paraphrased version with proper sampling
        outputs = paraphraser(
            text,
            max_length=256,
            num_return_sequences=1,
            do_sample=True,        # enables randomness
            temperature=0.9,       # controls creativity
            top_p=0.9              # nucleus sampling
        )

        return outputs[0]["generated_text"].strip()

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"


# Example run
if __name__ == "__main__":
    sample = "AI-generated content often feels repetitive and unnatural, but it can be improved through better rewriting."
    print("Original:", sample)
    print("Humanized:", humanize_text(sample))
