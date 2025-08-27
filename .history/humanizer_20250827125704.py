# humanizer.py
import random
import re
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from difflib import SequenceMatcher
import string

# Make sure required NLTK data is downloaded
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

class TextHumanizer:
    def __init__(self, target_similarity_range=(0.50, 0.55)):
        self.target_similarity_range = target_similarity_range
        self.filler_words = [
            "actually", "basically", "to be honest", "in fact", "overall", 
            "you know", "like", "well", "so", "um", "uh", "right", "anyway",
            "frankly", "honestly", "seriously", "literally", "obviously"
        ]
        
        self.sentence_starters = [
            "I think", "In my opinion", "From what I understand", 
            "It seems like", "Apparently", "According to", "You see",
            "The thing is", "What I mean is", "Let me explain"
        ]
        
        self.connectors = [
            "however", "moreover", "furthermore", "additionally", 
            "besides", "also", "plus", "on top of that", "not to mention",
            "what's more", "in addition", "as well as"
        ]
        
        # Set a fixed seed for consistent results
        random.seed(42)
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def synonym_replace(self, word, pos_tag=None):
        """Replace a word with a contextually appropriate synonym"""
        if not word.isalpha() or len(word) < 3:
            return word
            
        # Get synonyms based on POS tag if available
        if pos_tag and pos_tag.startswith(('NN', 'VB', 'JJ')):
            # Convert NLTK POS tags to WordNet POS tags
            pos_mapping = {'NN': 'n', 'VB': 'v', 'JJ': 'a', 'RB': 'r'}
            wn_pos = pos_mapping.get(pos_tag[:2], None)
            if wn_pos:
                synsets = wordnet.synsets(word, pos=wn_pos)
            else:
                synsets = wordnet.synsets(word)
        else:
            synsets = wordnet.synsets(word)
            
        if not synsets:
            return word
            
        # Get all possible synonyms
        synonyms = set()
        for syn in synsets:
            for lemma in syn.lemmas():
                if lemma.name().lower() != word.lower() and len(lemma.name()) > 2:
                    synonyms.add(lemma.name().replace("_", " "))
        
        return random.choice(list(synonyms)) if synonyms else word
    
    def restructure_sentences(self, sentences):
        """Restructure sentences for more human-like flow"""
        if len(sentences) <= 1:
            return sentences
            
        restructured = []
        for i, sentence in enumerate(sentences):
            # Randomly add sentence starters
            if random.random() < 0.3:
                starter = random.choice(self.sentence_starters)
                sentence = f"{starter}, {sentence.lower()}"
            
            # Randomly add connectors between sentences
            if i > 0 and random.random() < 0.4:
                connector = random.choice(self.connectors)
                sentence = f"{connector}, {sentence.lower()}"
            
            restructured.append(sentence)
        
        return restructured
    
    def add_human_patterns(self, text):
        """Add human-like speech patterns"""
        # Add contractions
        text = re.sub(r'\b(I am|you are|he is|she is|it is|we are|they are)\b', 
                     lambda m: m.group(1).split()[0] + "'" + m.group(1).split()[1][0] + m.group(1).split()[1][1:], 
                     text, flags=re.IGNORECASE)
        
        # Add informal expressions
        informal_patterns = [
            (r'\b(very|extremely)\b', 'pretty'),
            (r'\b(important)\b', 'big deal'),
            (r'\b(problem)\b', 'issue'),
            (r'\b(situation)\b', 'thing'),
            (r'\b(utilize)\b', 'use'),
            (r'\b(implement)\b', 'put in place'),
            (r'\b(optimize)\b', 'make better'),
            (r'\b(leverage)\b', 'use'),
            (r'\b(synergy)\b', 'working together'),
            (r'\b(paradigm)\b', 'way of thinking'),
        ]
        
        for pattern, replacement in informal_patterns:
            if random.random() < 0.7:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

    # ===== Heading-aware processing =====
    def _is_heading_line(self, line: str) -> bool:
        s = line.strip()
        if not s:
            return False
        # Indicators of headings: emojis, trailing colon, short length, title case, all caps
        if any(s.startswith(mark) for mark in ["#", "🧠", "📌", "⚙️", "🛠", "🚀", "📊", "🔮"]):
            return True
        if s.endswith(":") and len(s) <= 120:
            return True
        # All caps (ignoring non letters)
        letters = ''.join(ch for ch in s if ch.isalpha())
        if letters and letters.isupper():
            return True
        # Title-ish and short
        if len(s) <= 80 and sum(1 for w in s.split() if w[:1].isupper()) >= max(1, len(s.split())//2):
            return True
        return False

    def _parse_sections(self, text: str):
        lines = text.splitlines()
        sections = []
        current_heading = None
        current_lines = []
        for line in lines:
            if self._is_heading_line(line):
                if current_heading is not None or current_lines:
                    sections.append((current_heading, "\n".join(current_lines).strip()))
                    current_lines = []
                current_heading = line.strip()
            else:
                current_lines.append(line)
        # flush last
        if current_heading is not None or current_lines:
            sections.append((current_heading, "\n".join(current_lines).strip()))
        # If no headings detected, single section with no heading
        if not sections:
            sections = [(None, text.strip())]
        return sections

    def _capitalize_first_letter(self, s: str) -> str:
        i = 0
        while i < len(s) and s[i].isspace():
            i += 1
        if i < len(s):
            return s[:i] + s[i].upper() + s[i+1:]
        return s

    def _postprocess_text(self, text: str) -> str:
        # Trim spaces at line ends and starts
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        # Collapse multiple spaces (not newlines)
        text = re.sub(r"[ \t]{2,}", " ", text)
        # Remove space before punctuation
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        # Ensure space after punctuation when followed by non-space
        text = re.sub(r"([,.;:!?])(\S)", r"\1 \2", text)
        # Normalize parentheses spacing: no extra inside, one space outside if needed
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)
        # Collapse 3+ newlines to 2
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Capitalize first letter of each paragraph
        paragraphs = text.split("\n\n")
        paragraphs = [self._capitalize_first_letter(p.strip()) for p in paragraphs]
        text = "\n\n".join(paragraphs)
        # Final trim
        return text.strip()

    def humanize_with_headings(self, text: str):
        original_text = text.strip()
        sections = self._parse_sections(original_text)
        humanized_sections = []
        for heading, content in sections:
            if content:
                humanized_content, _ = self.humanize_text(content)
            else:
                humanized_content = ""
            humanized_sections.append((heading, humanized_content))
        # Reconstruct with spacing: heading, blank line, content, blank line
        parts = []
        for heading, content in humanized_sections:
            if heading:
                parts.append(heading)
            if content:
                if parts and parts[-1] == heading:
                    parts.append("")  # blank line between heading and content
                parts.append(content)
            parts.append("")  # section separator
        humanized_full = "\n".join(parts).strip()
        humanized_full = self._postprocess_text(humanized_full)
        similarity = self.calculate_similarity(original_text, humanized_full)
        return humanized_full, similarity
    
    def humanize_text(self, text):
        """Main function to humanize text with controlled similarity"""
        original_text = text.strip()
        
        # Multiple transformation attempts to achieve target similarity
        for attempt in range(15):
            # Step 1: Break into sentences
            sentences = sent_tokenize(original_text)
            
            # Step 2: Apply aggressive word-level transformations
            transformed_sentences = []
            for sentence in sentences:
                words = word_tokenize(sentence)
                pos_tags = nltk.pos_tag(words)
                
                new_words = []
                for word, pos_tag in pos_tags:
                    # Much higher probability of synonym replacement
                    if word.isalpha() and len(word) > 3 and random.random() < 0.7:
                        new_word = self.synonym_replace(word, pos_tag)
                        new_words.append(new_word)
                    else:
                        new_words.append(word)
                
                # Add filler words more frequently
                if random.random() < 0.6:
                    filler = random.choice(self.filler_words)
                    new_words.insert(0, filler)
                
                transformed_sent = " ".join(new_words)
                transformed_sentences.append(transformed_sent)
            
            # Step 3: Aggressive sentence restructuring
            restructured_sentences = self.restructure_sentences(transformed_sentences)
            
            # Step 4: Join and add human patterns
            humanized_text = " ".join(restructured_sentences)
            humanized_text = self.add_human_patterns(humanized_text)
            
            # Step 5: Additional transformations to reduce similarity
            if attempt > 5:
                # Add more sentence starters and connectors
                humanized_text = self.add_more_human_elements(humanized_text)
                
                # Randomly change sentence order
                if len(sentences) > 1 and random.random() < 0.5:
                    humanized_text = self.reorder_sentences(humanized_text)
            
            # Step 6: Check similarity
            similarity = self.calculate_similarity(original_text, humanized_text)
            
            # If similarity is in target range, return the result
            if self.target_similarity_range[0] <= similarity <= self.target_similarity_range[1]:
                return self._postprocess_text(humanized_text), similarity
            
            # If similarity is still too high, apply even more aggressive transformations
            if similarity > self.target_similarity_range[1]:
                # Add more informal language and contractions
                humanized_text = self.add_human_patterns(humanized_text)
                humanized_text = self.add_human_patterns(humanized_text)  # Apply twice
                
                # Add random punctuation and spacing variations
                if random.random() < 0.5:
                    humanized_text = humanized_text.replace(".", "...").replace("!", "!!")
                    humanized_text = humanized_text.replace("and", "&").replace("or", "/")
                
                # Add more filler words
                words = humanized_text.split()
                if len(words) > 5:
                    insert_pos = random.randint(0, len(words)//2)
                    words.insert(insert_pos, random.choice(self.filler_words))
                    humanized_text = " ".join(words)
        
        # If we can't achieve target similarity after 15 attempts, return the best result
        return self._postprocess_text(humanized_text), self.calculate_similarity(original_text, humanized_text)
    
    def add_more_human_elements(self, text):
        """Add more human-like elements to further reduce similarity"""
        # Add more informal expressions
        informal_replacements = [
            (r'\b(technology)\b', 'tech stuff'),
            (r'\b(application)\b', 'app'),
            (r'\b(implementation)\b', 'putting in place'),
            (r'\b(optimization)\b', 'making better'),
            (r'\b(utilization)\b', 'using'),
            (r'\b(comprehensive)\b', 'complete'),
            (r'\b(sophisticated)\b', 'fancy'),
            (r'\b(innovative)\b', 'new and cool'),
            (r'\b(efficient)\b', 'good at doing things'),
            (r'\b(automated)\b', 'done by itself'),
        ]
        
        for pattern, replacement in informal_replacements:
            if random.random() < 0.8:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def reorder_sentences(self, text):
        """Randomly reorder sentences to reduce similarity"""
        sentences = sent_tokenize(text)
        if len(sentences) > 1:
            random.shuffle(sentences)
        return " ".join(sentences)


def humanize_text(text):
    """Wrapper function for backward compatibility"""
    humanizer = TextHumanizer()
    humanized_text, similarity = humanizer.humanize_text(text)
    return humanized_text
