import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

class AIHumanizer:
    def __init__(self, model_name="Vamsi/T5_Paraphrase_Paws", device=None):
        # Load tokenizer & model
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

        # Set device
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = self.model.to(self.device)

    def humanize(self, text: str) -> str:
        """Convert AI-generated text into a more human-like version."""

        if not text.strip():
            return "[Error] Empty input text."

        # Prepare input
        input_text = "paraphrase: " + text + " </s>"
        encoding = self.tokenizer.encode_plus(
            input_text,
            padding="longest",
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        input_ids, attention_mask = encoding["input_ids"].to(self.device), encoding["attention_mask"].to(self.device)

        # Safe beam search (fix: num_return_sequences ≤ num_beams)
        num_beams = 5
        num_return_sequences = min(3, num_beams)  # ensure valid

        try:
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=256,
                num_beams=num_beams,
                num_return_sequences=num_return_sequences,
                temperature=0.9,
                top_p=0.95,
                top_k=50,
                early_stopping=True
            )

            # Decode all outputs
            paraphrases = [self.tokenizer.decode(out, skip_special_tokens=True) for out in outputs]

            # Return the best variation (or join multiple if you want)
            return paraphrases[0] if paraphrases else "[Error] No output generated."

        except Exception as e:
            return f"[Error] Failed to humanize text → {str(e)}"
