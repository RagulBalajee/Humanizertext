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

    # ===== Heading and list-aware processing =====
    def _is_heading_line(self, line: str) -> bool:
        s = line.strip()
        if not s:
            return False
        if any(s.startswith(mark) for mark in ["#", "🧠", "📌", "⚙️", "🛠", "🚀", "📊", "🔮"]):
            return True
        if s.endswith(":") and len(s) <= 120:
            return True
        letters = ''.join(ch for ch in s if ch.isalpha())
        if letters and letters.isupper():
            return True
        if len(s) <= 80 and sum(1 for w in s.split() if w[:1].isupper()) >= max(1, len(s.split())//2):
            return True
        return False

    def _is_list_item(self, line: str) -> bool:
        s = line.strip()
        if not s:
            return False
        if re.match(r"^[-*•]\s+", s):
            return True
        if re.match(r"^\d+[\.)]\s+", s):
            return True
        if re.match(r"^[\u2022\u25CF\u25AA]\s+", s):
            return True
        return False

    def _split_list_items(self, text: str):
        lines = text.splitlines()
        groups = []
        current = []
        in_list = False
        for line in lines:
            if self._is_list_item(line):
                in_list = True
                if current and not self._is_list_item(current[-1]):
                    groups.append((False, "\n".join(current).strip()))
                    current = []
                current.append(line)
            else:
                if in_list and current and self._is_list_item(current[-1]):
                    groups.append((True, "\n".join(current).strip()))
                    current = []
                    in_list = False
                current.append(line)
        if current:
            groups.append((in_list, "\n".join(current).strip()))
        return groups

    def _humanize_list_block(self, block: str) -> str:
        out_lines = []
        for line in block.splitlines():
            prefix = ""
            content = line.strip()
            m = re.match(r"^([-*•]|\d+[\.)]|[\u2022\u25CF\u25AA])\s+(.*)$", content)
            if m:
                marker, item = m.group(1), m.group(2)
                prefix = f"{marker} "
            else:
                item = content
            humanized, _ = self.humanize_text(item)
            humanized = self._capitalize_first_letter(humanized)
            out_lines.append(prefix + humanized)
        return "\n".join(out_lines)

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
        if current_heading is not None or current_lines:
            sections.append((current_heading, "\n".join(current_lines).strip()))
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
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        text = re.sub(r"([,.;:!?])(\S)", r"\1 \2", text)
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        paragraphs = text.split("\n\n")
        paragraphs = [self._capitalize_first_letter(p.strip()) for p in paragraphs]
        text = "\n\n".join(paragraphs)
        return text.strip()

    def humanize_with_headings(self, text: str):
        original_text = text.strip()
        sections = self._parse_sections(original_text)
        humanized_sections = []
        for heading, content in sections:
            if content:
                # Preserve list structure inside each section
                blocks = self._split_list_items(content)
                humanized_blocks = []
                for is_list, block in blocks:
                    if not block:
                        continue
                    if is_list:
                        humanized_blocks.append(self._humanize_list_block(block))
                    else:
                        humanized_block, _ = self.humanize_text(block)
                        humanized_blocks.append(humanized_block)
                humanized_content = "\n".join(humanized_blocks).strip()
            else:
                humanized_content = ""
            humanized_sections.append((heading, humanized_content))
        parts = []
        for heading, content in humanized_sections:
            if heading:
                parts.append(heading)
            if content:
                if parts and parts[-1] == heading:
                    parts.append("")
                parts.append(content)
            parts.append("")
        humanized_full = "\n".join(parts).strip()
        humanized_full = self._postprocess_text(humanized_full)
        similarity = self.calculate_similarity(original_text, humanized_full)
        return humanized_full, similarity
    
    def humanize_text(self, text):
        """Main function to humanize text with controlled similarity"""
        original_text = text.strip()
        
        for attempt in range(15):
            sentences = sent_tokenize(original_text)
            transformed_sentences = []
            for sentence in sentences:
                words = word_tokenize(sentence)
                pos_tags = nltk.pos_tag(words)
                new_words = []
                for word, pos_tag in pos_tags:
                    if word.isalpha() and len(word) > 3 and random.random() < 0.7:
                        new_word = self.synonym_replace(word, pos_tag)
                        new_words.append(new_word)
                    else:
                        new_words.append(word)
                if random.random() < 0.6:
                    filler = random.choice(self.filler_words)
                    new_words.insert(0, filler)
                transformed_sent = " ".join(new_words)
                transformed_sentences.append(transformed_sent)
            restructured_sentences = self.restructure_sentences(transformed_sentences)
            humanized_text = " ".join(restructured_sentences)
            humanized_text = self.add_human_patterns(humanized_text)
            if attempt > 5:
                humanized_text = self.add_more_human_elements(humanized_text)
                if len(sentences) > 1 and random.random() < 0.5:
                    humanized_text = self.reorder_sentences(humanized_text)
            similarity = self.calculate_similarity(original_text, humanized_text)
            if self.target_similarity_range[0] <= similarity <= self.target_similarity_range[1]:
                return self._postprocess_text(humanized_text), similarity
            if similarity > self.target_similarity_range[1]:
                humanized_text = self.add_human_patterns(humanized_text)
                humanized_text = self.add_human_patterns(humanized_text)
                if random.random() < 0.5:
                    humanized_text = humanized_text.replace(".", "...").replace("!", "!!")
                    humanized_text = humanized_text.replace("and", "&").replace("or", "/")
                words = humanized_text.split()
                if len(words) > 5:
                    insert_pos = random.randint(0, len(words)//2)
                    words.insert(insert_pos, random.choice(self.filler_words))
                    humanized_text = " ".join(words)
        return self._postprocess_text(humanized_text), self.calculate_similarity(original_text, humanized_text)
    
    def add_more_human_elements(self, text):
        """Add more human-like elements to further reduce similarity"""
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
        sentences = sent_tokenize(text)
        if len(sentences) > 1:
            random.shuffle(sentences)
        return " ".join(sentences)


def humanize_text(text):
    humanizer = TextHumanizer()
    humanized_text, similarity = humanizer.humanize_text(text)
    return humanized_text
