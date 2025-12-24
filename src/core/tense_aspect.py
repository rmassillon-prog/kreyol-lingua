"""
Tense-Aspect-Mood (TAM) System for Haitian Creole
================================================

Handles identification and normalization of TAM markers.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Set
import json
from pathlib import Path


class TAMCategory(Enum):
    """Categories of TAM markers in Haitian Creole"""
    PROGRESSIVE = "progressive"      # ap, a
    PAST = "past"                   # te, t
    FUTURE = "future"               # pral, prale, ral, rale, a (context)
    IRREALIS = "irrealis"           # ta
    COMPLETIVE = "completive"       # fin, fini
    ABILITY = "ability"             # kapab, ka, kab


@dataclass(frozen=True)
class TAMTag:
    """
    Abstract representation of a TAM marker.
    """
    category: TAMCategory
    canonical: str  # Standard written form
    
    def __str__(self) -> str:
        """Return abstract tag format: TAM_PROG, TAM_PAST, etc."""
        mapping = {
            TAMCategory.PROGRESSIVE: "TAM_PROG",
            TAMCategory.PAST: "TAM_PAST",
            TAMCategory.FUTURE: "TAM_FUT",
            TAMCategory.IRREALIS: "TAM_IRR",
            TAMCategory.COMPLETIVE: "TAM_COMPL",
            TAMCategory.ABILITY: "TAM_ABIL",
        }
        return mapping.get(self.category, f"TAM_{self.category.name}")
    
    def __repr__(self) -> str:
        return f"TAMTag({self.category.value}, '{self.canonical}')"


@dataclass
class TAMForm:
    """Information about a specific TAM surface form"""
    surface: str
    tag: TAMTag
    note: Optional[str] = None
    is_fused: bool = False  # e.g., "ap" can fuse with pronouns


class TAMMapper:
    """
    Central TAM marker normalization system.
    """
    
    # Valid TAM combinations (order matters!)
    VALID_COMBINATIONS = {
        ('te', 'ap'),      # Past progressive: "te ap" ✓
        ('te', 'pral'),    # Past future: "te pral" ✓
        ('ta', 'ap'),      # Irrealis progressive: "ta ap" ✓
        # Invalid combinations caught:
        # ('ap', 'te') - WRONG ORDER
        # ('pral', 'te') - WRONG ORDER
    }
    
    def __init__(self, lexicon_path: Optional[Path] = None):
        """
        Initialize the TAM mapper.
        
        Args:
            lexicon_path: Path to tense_aspect.json file
        """
        if lexicon_path is None:
            lexicon_path = Path(__file__).parent.parent.parent / "data" / "lexicon" / "tense_aspect.json"
        
        self.lexicon_path = lexicon_path
        self.forms: Dict[str, TAMForm] = {}
        self._load_lexicon()
    
    def _load_lexicon(self) -> None:
        """Load TAM data from JSON file"""
        if not self.lexicon_path.exists():
            self._initialize_fallback()
            return
        
        with open(self.lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for surface, info in data.get("surface_forms", {}).items():
            tag = TAMTag(
                category=TAMCategory(info["category"]),
                canonical=info["canonical"]
            )
            
            form = TAMForm(
                surface=surface,
                tag=tag,
                note=info.get("note"),
                is_fused=info.get("is_fused", False)
            )
            
            self.forms[surface.lower()] = form
    
    def _initialize_fallback(self) -> None:
        """Fallback TAM data if JSON file not available"""
        fallback_data = {
            # Progressive
            'ap': (TAMCategory.PROGRESSIVE, 'ap', True),
            'a': (TAMCategory.PROGRESSIVE, 'ap', True),
            
            # Past
            'te': (TAMCategory.PAST, 'te', True),
            't': (TAMCategory.PAST, 'te', True),
            
            # Future
            'pral': (TAMCategory.FUTURE, 'pral', False),
            'prale': (TAMCategory.FUTURE, 'pral', False),
            'ral': (TAMCategory.FUTURE, 'pral', False),
            'rale': (TAMCategory.FUTURE, 'pral', False),
            'a': (TAMCategory.FUTURE, 'pral', True),  # Context-dependent
            
            # Irrealis
            'ta': (TAMCategory.IRREALIS, 'ta', False),
            
            # Completive
            'fin': (TAMCategory.COMPLETIVE, 'fin', False),
            'fini': (TAMCategory.COMPLETIVE, 'fin', False),
            
            # Ability
            'kapab': (TAMCategory.ABILITY, 'kapab', False),
            'ka': (TAMCategory.ABILITY, 'kapab', False),
            'kab': (TAMCategory.ABILITY, 'kapab', False),
        }
        
        for surface, (category, canonical, is_fused) in fallback_data.items():
            tag = TAMTag(category=category, canonical=canonical)
            self.forms[surface] = TAMForm(
                surface=surface,
                tag=tag,
                is_fused=is_fused
            )
    
    def normalize(self, surface_form: str) -> Optional[TAMTag]:
        """
        Convert surface form to abstract TAM tag.
        
        Args:
            surface_form: The TAM marker as it appears in text
            
        Returns:
            TAMTag if recognized, None otherwise
        """
        form = self.forms.get(surface_form.lower())
        return form.tag if form else None
    
    def get_form_info(self, surface_form: str) -> Optional[TAMForm]:
        """Get complete information about a TAM form"""
        return self.forms.get(surface_form.lower())
    
    def get_canonical_form(self, surface_form: str) -> Optional[str]:
        """Get the canonical/standard written form"""
        tag = self.normalize(surface_form)
        return tag.canonical if tag else None
    
    def can_fuse(self, surface_form: str) -> bool:
        """Check if this TAM marker can fuse with pronouns"""
        form = self.get_form_info(surface_form)
        return form.is_fused if form else False
    
    def validate_combination(self, markers: List[str]) -> tuple[bool, Optional[str]]:
        """
        Validate a sequence of TAM markers.
        
        Args:
            markers: List of TAM markers in order
            
        Returns:
            (is_valid, error_message)
        """
        if len(markers) < 2:
            return (True, None)
        
        # Get canonical forms
        canonical_markers = []
        for marker in markers:
            canonical = self.get_canonical_form(marker)
            if canonical:
                canonical_markers.append(canonical)
        
        # Check if combination is valid
        combination = tuple(canonical_markers)
        
        if combination not in self.VALID_COMBINATIONS:
            return (False, f"Invalid TAM combination: {' + '.join(markers)}")
        
        return (True, None)
    
    def get_all_forms_for_tag(self, tag: TAMTag) -> List[str]:
        """Get all surface forms that map to a given tag"""
        return [
            form.surface 
            for form in self.forms.values() 
            if form.tag == tag
        ]


if __name__ == "__main__":
    # Test the TAM mapper
    mapper = TAMMapper()
    
    print("=== TAM Normalization Examples ===")
    test_forms = ["ap", "a", "te", "t", "pral", "ral", "ta", "fin", "kapab"]
    
    for form in test_forms:
        tag = mapper.normalize(form)
        canonical = mapper.get_canonical_form(form)
        can_fuse = mapper.can_fuse(form)
        
        print(f"{form:6} → {tag}  (canonical: {canonical}, can_fuse: {can_fuse})")
    
    print("\n=== TAM Combination Validation ===")
    test_combinations = [
        ["te", "ap"],      # Valid
        ["ap", "te"],      # Invalid (wrong order)
        ["ta", "ap"],      # Valid
        ["pral", "te"],    # Invalid
    ]
    
    for combo in test_combinations:
        is_valid, error = mapper.validate_combination(combo)
        status = "✓" if is_valid else "✗"
        msg = f"{status} {' + '.join(combo)}"
        if error:
            msg += f" - {error}"
        print(msg)

