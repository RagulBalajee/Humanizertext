from transformers import pipeline

# Load the paraphrasing model
paraphraser = pipeline(
    "text2text-generation",
    model="Vamsi/T5_Paraphrase_Paws",
    device=0  # use GPU/MPS if available, else CPU
)

def humanize_text(text: str) -> str:
    """
    Takes AI-generated text and rewrites it into a more human-like version.
    Uses diverse decoding strategies for better variation.
    """
    if not text.strip():
        return "[Error] Empty input text."

    try:
        # Generate a paraphrased version
        outputs = paraphraser(
            text,
            max_length=256,
            num_beams=5,           # beam search for quality
            num_return_sequences=1,
            do_sample=True,        # add randomness
            temperature=0.8,       # control creativity
            top_p=0.92,            # nucleus sampling
            repetition_penalty=1.15  # reduces repetition
        )

        return outputs[0]["generated_text"].strip()

    except Exception as e:
        return f"[Error] Failed to humanize text → {str(e)}"


if __name__ == "__main__":
    print("🤖 AI to Human Content Converter")
    print("Type 'exit' anytime to quit.\n")

    while True:
        text = input("Enter AI-generated text:\n> ")
        if text.lower().strip() == "exit":
            print("Goodbye 👋")
            break

        humanized = humanize_text(text)
        print("\n✨ Humanized Content:\n")
        print(humanized)
        print("-" * 60)
