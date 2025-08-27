import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random

class AIHumanizer:
    def __init__(self, model_name="t5-base"):
        print("Loading model... (this may take a few seconds)")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.model.to(self.device)

    def humanize(self, text):
        # Add a "paraphrase" instruction to force rewording
        prompt = f"Paraphrase this text in a more human-like, casual style:\n{text}"

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)

        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=256,
            num_beams=4,
            num_return_sequences=1,
            do_sample=True,            # Enable sampling (forces randomness)
            top_k=50,                  # Keep top 50 words for randomness
            top_p=0.92,                # Nucleus sampling
            temperature=1.2,           # Higher = more variation
            early_stopping=True
        )

        humanized = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Post-processing: Add more randomness
        humanized = self._postprocess(humanized)

        return humanized.strip()

    def _postprocess(self, text):
        # Add filler words randomly to break "AI-smoothness"
        fillers = [
            "to be honest", "actually", "in simple terms", 
            "you could say", "in real life", "basically"
        ]
        sentences = text.split(". ")
        for i in range(len(sentences)):
            if random.random() < 0.3:  # 30% chance to add filler
                sentences[i] = fillers[random.randint(0, len(fillers)-1)] + ", " + sentences[i]
        return ". ".join(sentences)
