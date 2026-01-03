import sys
from pathlib import Path

# Add the project root to python path so we can import src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.database import DatabaseManager

def seed():
    print("🌱 Seeding database...")
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()

    # The Initial Vocabulary List
    # format: (word, pos, definition, english)
    words = [
        ("manje", "VERB", "To eat or food", "eat"),
        ("dlo", "NOUN", "Water", "water"),
        ("kriye", "VERB", "To cry", "cry"),
        ("mache", "VERB", "To walk", "walk"),
        ("lakay", "NOUN", "Home", "home"),
        ("travay", "VERB", "To work", "work"),
        ("liv", "NOUN", "Book", "book"),
        ("lekòl", "NOUN", "School", "school")
    ]

    count = 0
    for w in words:
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO lexicon (word, pos, definition, english) VALUES (?, ?, ?, ?)",
                w
            )
            count += 1
        except Exception as e:
            print(f"Error adding {w[0]}: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Successfully added {count} words to the Brain!")

if __name__ == "__main__":
    seed()
