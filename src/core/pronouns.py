"""
Pronoun and Clitic System for Haitian Creole
===========================================

Handles:
- Surface form → abstract tag mapping
- Independent vs. dependent clitic distinction
- Validation of clitic usage contexts
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List
import json
from pathlib import Path


class Person(Enum):
    """Grammatical person"""
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Number(Enum):
    """Grammatical number"""
    SINGULAR = "SG"
    PLURAL = "PL"


class PronounType(Enum):
    """Type of pronoun form"""
    INDEPENDENT = "independent"              # mwen, ou, li, nou, yo
    INDEPENDENT_REDUCED = "independent_reduced"  # m (valid standalone)
    DEPENDENT_CLITIC = "dependent_clitic"    # w, l, n, y (must attach)


@dataclass(frozen=True)
class PronounTag:
    """
    Abstract representation of a pronoun.
    
    All surface forms map to this internal representation.
    """
    person: Person
    number: Number
    canonical: str  # The standard written form
    
    def __str__(self) -> str:
        """Return abstract tag format: PRON_1SG, PRON_2PL, etc."""
        return f"PRON_{self.person.value}{self.number.value}"
    
    def __repr__(self) -> str:
        return f"PronounTag({self.person.name}, {self.number.value}, '{self.canonical}')"


@dataclass
class PronounForm:
    """
    Information about a specific surface form.
    """
    surface: str
    tag: PronounTag
    form_type: PronounType
    note: Optional[str] = None
    
    def is_clitic(self) -> bool:
        """Check if this is a dependent clitic"""
        return self.form_type == PronounType.DEPENDENT_CLITIC
    
    def can_stand_alone(self) -> bool:
        """Check if this form can appear independently"""
        return self.form_type in [
            PronounType.INDEPENDENT,
            PronounType.INDEPENDENT_REDUCED
        ]


class PronounMapper:
    """
    Central pronoun normalization system.
    """
    
    def __init__(self, lexicon_path: Optional[Path] = None):
        """
        Initialize the pronoun mapper.
        
        Args:
            lexicon_path: Path to pronouns.json file.
        """
        if lexicon_path is None:
            lexicon_path = Path(__file__).parent.parent.parent / "data" / "lexicon" / "pronouns.json"
        
        self.lexicon_path = lexicon_path
        self.forms: Dict[str, PronounForm] = {}
        self._load_lexicon()
    
    def _load_lexicon(self) -> None:
        """Load pronoun data from JSON file"""
        if not self.lexicon_path.exists():
            self._initialize_fallback()
            return
        
        with open(self.lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for surface, info in data.get("surface_forms", {}).items():
            tag = PronounTag(
                person=Person(info["person"]),
                number=Number(info["number"]),
                canonical=info["canonical"]
            )
            
            form = PronounForm(
                surface=surface,
                tag=tag,
                form_type=PronounType(info["type"]),
                note=info.get("note")
            )
            
            self.forms[surface.lower()] = form
    
    def _initialize_fallback(self) -> None:
        """Fallback pronoun data if JSON file not available"""
        fallback_data = {
            # First person singular
            'mwen': (Person.FIRST, Number.SINGULAR, 'mwen', PronounType.INDEPENDENT),
            'moin': (Person.FIRST, Number.SINGULAR, 'mwen', PronounType.INDEPENDENT),
            'm': (Person.FIRST, Number.SINGULAR, 'mwen', PronounType.INDEPENDENT_REDUCED),
            
            # Second person singular
            'ou': (Person.SECOND, Number.SINGULAR, 'ou', PronounType.INDEPENDENT),
            'w': (Person.SECOND, Number.SINGULAR, 'ou', PronounType.DEPENDENT_CLITIC),
            
            # Third person singular
            'li': (Person.THIRD, Number.SINGULAR, 'li', PronounType.INDEPENDENT),
            'l': (Person.THIRD, Number.SINGULAR, 'li', PronounType.DEPENDENT_CLITIC),
            
            # First person plural
            'nou': (Person.FIRST, Number.PLURAL, 'nou', PronounType.INDEPENDENT),
            'n': (Person.FIRST, Number.PLURAL, 'nou', PronounType.DEPENDENT_CLITIC),
            
            # Third person plural
            'yo': (Person.THIRD, Number.PLURAL, 'yo', PronounType.INDEPENDENT),
            'y': (Person.THIRD, Number.PLURAL, 'yo', PronounType.DEPENDENT_CLITIC),
        }
        
        for surface, (person, number, canonical, pron_type) in fallback_data.items():
            tag = PronounTag(person=person, number=number, canonical=canonical)
            self.forms[surface] = PronounForm(
                surface=surface,
                tag=tag,
                form_type=pron_type
            )
    
    def normalize(self, surface_form: str) -> Optional[PronounTag]:
        """
        Convert surface form to abstract pronoun tag.
        
        Args:
            surface_form: The pronoun as it appears in text
            
        Returns:
            PronounTag if recognized, None otherwise
        """
        form = self.forms.get(surface_form.lower())
        return form.tag if form else None
    
    def get_form_info(self, surface_form: str) -> Optional[PronounForm]:
        """Get complete information about a pronoun form"""
        return self.forms.get(surface_form.lower())
    
    def is_clitic(self, surface_form: str) -> bool:
        """Check if a form is a dependent clitic"""
        form = self.get_form_info(surface_form)
        return form.is_clitic() if form else False
    
    def validate_clitic_context(
        self, 
        surface_form: str, 
        preceding_token: Optional[str] = None,
        following_token: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate that a clitic appears in a legal context.
        
        Returns:
            (is_valid, error_message)
        """
        form = self.get_form_info(surface_form)
        
        if not form:
            return (True, None)
        
        if not form.is_clitic():
            return (True, None)
        
        if preceding_token is None and following_token is None:
            return (False, f"Clitic '{surface_form}' cannot stand alone")
        
        return (True, None)
    
    def get_canonical_form(self, surface_form: str) -> Optional[str]:
        """Get the canonical/standard written form"""
        tag = self.normalize(surface_form)
        return tag.canonical if tag else None
    
    def get_all_forms_for_tag(self, tag: PronounTag) -> List[str]:
        """Get all surface forms that map to a given tag"""
        return [
            form.surface 
            for form in self.forms.values() 
            if form.tag == tag
        ]


if __name__ == "__main__":
    # Test the pronoun mapper
    mapper = PronounMapper()
    
    print("=== Pronoun Normalization Examples ===")
    test_forms = ["mwen", "moin", "m", "ou", "w", "li", "l"]
    
    for form in test_forms:
        tag = mapper.normalize(form)
        canonical = mapper.get_canonical_form(form)
        is_clitic = mapper.is_clitic(form)
        
        print(f"{form:6} → {tag}  (canonical: {canonical}, clitic: {is_clitic})")
