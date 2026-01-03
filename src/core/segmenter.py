from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SegmentationResult:
    is_valid: bool
    segments: List[str]


class Segmenter:
    """
    v1 segmenter: dictionary-based splitting for common fused forms.
    Expand later with rules + probabilities.
    """
    def __init__(self) -> None:
        self.lexicon = {
            # Common TAM/pronoun fusions:
            "map": ["m", "ap"],
            "m'ap": ["m", "ap"],
            "m’ap": ["m", "ap"],
            "nap": ["n", "ap"],
            "n'ap": ["n", "ap"],
            "n’ap": ["n", "ap"],
            "wap": ["w", "ap"],
            "w'ap": ["w", "ap"],
            "w’ap": ["w", "ap"],
            "lap": ["l", "ap"],
            "l'ap": ["l", "ap"],
            "l’ap": ["l", "ap"],
        }

    def segment(self, token: str) -> Optional[SegmentationResult]:
        key = token.lower()
        if key in self.lexicon:
            return SegmentationResult(is_valid=True, segments=self.lexicon[key])
        return None
