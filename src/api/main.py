from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
# Pointing to your new framework
from src.normalizer import analyze_text 

app = FastAPI(
    title="Kreyòl Lingua NLP Engine",
    description="API for normalizing and parsing Haitian Creole text",
    version="1.2"
)

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "online", "engine": "Kreyòl Lingua v1.2"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    # This now uses the Tokenizer and Thomas's phonetic fixes
    return analyze_text(request.text)
