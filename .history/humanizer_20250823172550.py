# humanizer.py

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# ✅ Device config (MPS for Mac, CUDA for GPU, else CPU)
device = 0 if torch.cuda.is_available() else -1

# ✅ Tone detection pipeline (zero-shot classification)
tone_detector = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

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

# Candidate tones we want to detect
candidate_tones = ["casual", "formal", "storytelling", "academic", "professional"]

def detect_tone(text: str) -> str:
    """Detect the most likely tone of the given text."""
    result = tone_detector(text, candidate_labels=candidate_tones)
    detected_tone = result["labels"][0]  # highest scoring label
    return detected_tone

def humanize_text(ai_text: str) -> str:
    """Detect tone and humanize AI text while keeping the tone."""
    detected_tone = detect_tone(ai_text)

    prompt = f"Paraphrase the following text in a {detected_tone} way so it sounds natural and human-written:\n{ai_text}"
    result = humanizer(
        prompt,
        max_length=256,
        num_return_sequences=1,
        clean_up_tokenization_spaces=True
    )
    return result[0]["generated_text"], detected_tone

def main():
    print("🤖 AI to Human Content Converter (Auto-Tone)")
    print("Type 'exit' anytime to quit.\n")

    while True:
        ai_text = input("Enter AI-generated text:\n> ")
        if ai_text.lower() == "exit":
            break

        humanized, tone = humanize_text(ai_text)
        print("\n✨ Detected Tone:", tone)
        print("\n✨ Humanized Content:\n")
        print(humanized)
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
