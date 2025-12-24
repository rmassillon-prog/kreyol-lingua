"""
Tokenization utilities for Haitian Creole
========================================
Simple, linguistically-aware tokenization.
"""
import re
from typing import List

def tokenize(text: str) -> List[str]:
    """
    Basic tokenization for Haitian Creole.
    
    Preserves apostrophes for segmentation (m'ap, l'ap, etc.)
    Splits on whitespace and punctuation.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List of tokens
    """
    if not text:
        return []
    
    # Pattern: Keep apostrophes with words, separate other punctuation
    # This preserves: m'ap, l'ap, n'ap, etc.
    pattern = r"[^\s.,!?;:«»\"()\[\]{}]+"
    
    tokens = re.findall(pattern, text)
    
    return tokens

def normalize_apostrophes(text: str) -> str:
    """
    Normalize different apostrophe characters to standard ASCII apostrophe.
    
    Haitian Creole texts may use: ' ' ` ʼ
    We normalize all to: '
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized apostrophes
    """
    # Common apostrophe variants
    apostrophe_variants = [
        "’",  # Right single quotation mark (Unicode U+2019)
        "‘",  # Left single quotation mark (Unicode U+2018)
        "`",  # Grave accent
        "ʼ",  # Modifier letter apostrophe (Unicode U+02BC)
    ]
    
    normalized = text
    for variant in apostrophe_variants:
        normalized = normalized.replace(variant, "'")
    
    return normalized

def detokenize(tokens: List[str]) -> str:
    """
    Simple detokenization - join tokens with spaces.
    
    Args:
        tokens: List of tokens
        
    Returns:
        Reconstructed text
    """
    return " ".join(tokens)

class CreoleTokenizer:
    """
    Stateful tokenizer with preprocessing options.
    """
    
    def __init__(self, normalize_apostrophes: bool = True):
        """
        Initialize tokenizer.
        
        Args:
            normalize_apostrophes: Whether to normalize apostrophe variants
        """
        self.normalize_apostrophes_flag = normalize_apostrophes
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text with preprocessing.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        if self.normalize_apostrophes_flag:
            text = normalize_apostrophes(text)
            
        return tokenize(text)
    
    def batch_tokenize(self, texts: List[str]) -> List[List[str]]:
        """
        Tokenize multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of token lists
        """
        return [self.tokenize(text) for text in texts]

if __name__ == "__main__":
    # Test tokenization
    print("=== Tokenization Examples ===")
    
    test_sentences = [
        "Mwen ap pale kreyòl.",
        "Map ale lakay mwen.",
        "Ou te wè li?",
        "M'ap travay jodi a.",
        "Li pral manje demen.",
    ]
    
    for sentence in test_sentences:
        tokens = tokenize(sentence)
        print(f"'{sentence}'")
        print(f"  -> {tokens}")
    print()
    
    print("=== Apostrophe Normalization ===")
    test_variants = [
        "M'ap ale",      # ASCII apostrophe
        "M’ap ale",      # Right single quote
        "M`ap ale",      # Grave accent
    ]
    
    for text in test_variants:
        normalized = normalize_apostrophes(text)
        print(f"'{text}' -> '{normalized}'")
