from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.core.normalizer import Normalizer

app = FastAPI(
    title="Kreyòl Lingua NLP Engine",
    description="API for normalizing and parsing Haitian Creole text",
    version="1.1"
)

# Initialize the Brain
normalizer = Normalizer()

class AnalyzeRequest(BaseModel):
    text: str

class TokenData(BaseModel):
    original: str
    normalized: str
    tags: List[str]

class AnalyzeResponse(BaseModel):
    original_text: str
    normalized_text: str
    tokens: List[TokenData]

@app.get("/")
def health_check():
    return {"status": "online", "engine": "Kreyòl Lingua v1.1"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = normalizer.normalize(request.text)
    
    api_tokens = []
    for t in result.tokens:
        tags = []
        # Add all our intelligent tags
        if t.pronoun_tag: tags.append(f"PRON:{t.pronoun_tag}")
        if t.tam_tag: tags.append(f"TAM:{t.tam_tag}")
        if t.pos_tag: tags.append(f"POS:{t.pos_tag}")         # New!
        if t.english_def: tags.append(f"DEF:{t.english_def}") # New!
        if t.is_segmented: tags.append("SEGMENTED")
        if t.is_unknown: tags.append("UNKNOWN")
        
        api_tokens.append(TokenData(
            original=t.original,
            normalized=t.normalized,
            tags=tags
        ))
        
    return AnalyzeResponse(
        original_text=result.original_text,
        normalized_text=result.get_normalized_text(),
        tokens=api_tokens
    )
