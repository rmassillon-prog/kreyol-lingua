import sqlite3
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Define where the database file will live
DB_PATH = Path("data/lexicon.db")

class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        # Ensure the data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self):
        """Create a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def _init_db(self):
        """Create the tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table 1: The Lexicon (Approved Creole Words)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lexicon (
            word TEXT PRIMARY KEY,
            pos TEXT NOT NULL,          -- Part of Speech (VERB, NOUN, etc.)
            definition TEXT,
            english TEXT,
            is_standard BOOLEAN DEFAULT 1
        );
        """)
        
        conn.commit()
        conn.close()

    def lookup_word(self, word: str) -> Optional[Dict[str, Any]]:
        """
        Search for a word in the database.
        Returns a dictionary like {'word': 'manje', 'pos': 'VERB'} or None.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM lexicon WHERE word = ?", (word.lower(),))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return dict(result)
        return None
