import sys
from pathlib import Path

# Add the project root to python path so we can import src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.database import DatabaseManager

def teach():
    print("\n🎓 Kreyòl Lingua - Teacher Mode")
    print("===============================")
    print("Type a word to teach the brain.")
    print("Press 'Ctrl + C' to quit anytime.\n")
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        while True:
            # 1. Get the Word
            word = input("👉 Enter Creole Word: ").strip().lower()
            if not word: continue
            
            # Check if we already know it
            existing = db.lookup_word(word)
            if existing:
                print(f"   ⚠️  I already know '{word}' as a {existing['pos']} ({existing['english']}).")
                confirm = input("   Overwrite? (y/n): ").lower()
                if confirm != 'y':
                    print("   Skipped.\n")
                    continue

            # 2. Get Grammar Details
            pos = input("   Part of Speech (VERB/NOUN/ADJ/ADV): ").strip().upper()
            english = input("   English Meaning: ").strip()
            
            # Optional full definition
            definition = input("   Full Definition (optional): ").strip()
            if not definition:
                definition = english  # Default to simple meaning

            # 3. Save to Brain
            try:
                cursor.execute(
                    "INSERT OR REPLACE INTO lexicon (word, pos, definition, english) VALUES (?, ?, ?, ?)",
                    (word, pos, definition, english)
                )
                conn.commit()
                print(f"   ✅ Learned: {word} -> {english}\n")
            except Exception as e:
                print(f"   ❌ Error: {e}\n")
                
    except KeyboardInterrupt:
        print("\n\n👋 Class dismissed! All words saved.")
        conn.close()

if __name__ == "__main__":
    teach()
