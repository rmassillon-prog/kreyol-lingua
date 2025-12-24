"""
Logging utilities for the Haitian Creole NLP pipeline.
Handles tracking of unknown terms and system errors.
"""
import logging
import os
from datetime import datetime
from pathlib import Path

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure main logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CreoleNLP")

def log_unknown_term(term: str, context: str = ""):
    """
    Log a term that was not found in the lexicon.
    These logs are vital for lexicon expansion.
    """
    msg = f"UNKNOWN_TERM: '{term}' | Context: {context}"
    
    # Log to main system log
    logger.warning(msg)
    
    # Also append to a dedicated review file for the linguist
    with open(LOG_DIR / "review_queue.txt", "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}\t{term}\t{context}\n")

def get_logger(name: str):
    """Get a named logger instance."""
    return logging.getLogger(name)

if __name__ == "__main__":
    # Test logging
    print("Testing logger...")
    log_unknown_term("schtroumpf", "Mwen pa konnen kisa yon schtroumpf ye.")
    print(f"Check {LOG_DIR}/review_queue.txt to see the logged term.")
