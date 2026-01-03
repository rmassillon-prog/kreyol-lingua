from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from src.utils.tokenizer import tokenize
from src.utils.logger import log_unknown_term
from src.core.pronouns import PronounMapper
from src.core.tense_aspect import TAMMapper
from src.core.segmenter import Segmenter
from src.core.database import DatabaseManager

@dataclass
class Token:
    original: str
    normalized: str
    is_unknown: bool = False
    pronoun_tag: Optional[str] = None
    tam_tag: Optional[str] = None
    pos_tag: Optional[str] = None
    english_def: Optional[str] = None
    is_segmented: bool = False
    original_fused_form: Optional[str] = None

@dataclass
class NormalizationResult:
    original_text: str
    tokens: List[Token]
    
    def get_normalized_text(self) -> str:
        return " ".join([t.normalized for t in self.tokens])

class Normalizer:
    def __init__(self):
        # Initialize modules
        self.pronoun_mapper = PronounMapper()
        self.tam_mapper = TAMMapper()
        self.segmenter = Segmenter()
        self.db = DatabaseManager()  # Connect to the Database
        
        self.spelling_fixes = {
            "vwati": "voiture",
            "manger": "manje",
            "kounyea": "kounye a",
            "kounya": "kounye a"
        }

    def normalize(self, text: str) -> NormalizationResult:
        raw_words = tokenize(text)
        final_tokens = []
        
        for word in raw_words:
            seg_result = self.segmenter.segment(word)
            if seg_result and seg_result.is_valid:
                for part in seg_result.segments:
                    token_obj = self._process_single_word(part)
                    token_obj.is_segmented = True
                    token_obj.original_fused_form = word
                    final_tokens.append(token_obj)
            else:
                final_tokens.append(self._process_single_word(word))

        return NormalizationResult(original_text=text, tokens=final_tokens)

    def _process_single_word(self, word: str) -> Token:
        clean_word = word.lower()
        
        # A. Check Spelling
        if clean_word in self.spelling_fixes:
            clean_word = self.spelling_fixes[clean_word]

        # B. Check Pronouns
        pronoun_tag = self.pronoun_mapper.normalize(clean_word)
        if pronoun_tag:
            canonical = self.pronoun_mapper.get_canonical_form(clean_word)
            return Token(original=word, normalized=canonical, pronoun_tag=pronoun_tag)

        # C. Check Tense/Aspect
        tam_tag = self.tam_mapper.normalize(clean_word)
        if tam_tag:
            canonical = self.tam_mapper.get_canonical_form(clean_word)
            return Token(original=word, normalized=canonical, tam_tag=tam_tag)

        # D. DATABASE LOOKUP (The New "Memory" Check)
        db_entry = self.db.lookup_word(clean_word)
        if db_entry:
            return Token(
                original=word,
                normalized=clean_word,
                pos_tag=db_entry['pos'],       # e.g., "VERB"
                english_def=db_entry['english'], # e.g., "eat"
                is_unknown=False
            )

        # E. Unknown
        is_unknown = False
        if clean_word.isalpha():
            log_unknown_term(clean_word, context="Normalizer")
            is_unknown = True

        return Token(original=word, normalized=clean_word, is_unknown=is_unknown)
