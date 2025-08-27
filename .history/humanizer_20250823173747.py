# humanizer.py

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# ✅ Device config (MPS for Mac, CUDA for GPU, else CPU)
device = 0 if torch.cuda.is_available() else -1

# ✅ Humanization model (paraphrasing / rewriting)
model_name = "Vamsi/T5_Paraphrase_Paws"  # lightweight paraphrasing model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

humanizer = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device
)

def humanize_text(ai_text: str) -> str:
    """Paraphrase AI text into human-like content."""
    prompt = f"Paraphrase the following text to make it sound natural and human-written:\n{ai_text}"
    result = humanizer(
        prompt,
        max_length=256,
        num_return_sequences=1,
        clean_up_tokenization_spaces=True
    )
    return result[0]["generated_text"]

def main():
    print("🤖 AI to Human Content Converter (No Tone Mode)")
    print("Type 'exit' anytime to quit.\n")

    while True:
        ai_text = input("Enter AI-generated text:\n> ")
        if ai_text.lower() == "exit":
            break

        humanized = humanize_text(ai_text)
        print("\n✨ Humanized Content:\n")
        print(humanized)
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
