from fastapi import FastAPI
from pipeline import KreyolEngine

app = FastAPI()

# Simple normalizer for now (safe)
def normalize_text(text: str) -> str:
    return text.lower().strip()

engine = KreyolEngine(
    normalizer=normalize_text,
    tam_module=None,
    clitic_module=None
)

@app.get("/")
def home():
    return {
        "message": "Kreyòl Lingua API is Live",
        "engine": engine.ENGINE_VERSION
    }

@app.post("/analyze")
def analyze_kreyol(payload: dict):
    text = payload.get("text", "")
    return engine.analyze(text)
