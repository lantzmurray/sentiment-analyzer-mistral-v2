from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Sentiment Analyzer API",
    description="AI-powered sentiment analysis using Mistral model via Ollama",
    version="1.0.0"
)

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

class SentimentRequest(BaseModel):
    text: str
    temperature: Optional[float] = 0.3

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: Optional[float] = None
    processing_time: float

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sentiment Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze/",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "healthy", "ollama": "connected"}
        else:
            return {"status": "degraded", "ollama": "unavailable"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Ollama service unavailable: {str(e)}")

@app.post("/analyze/", response_model=SentimentResponse)
async def analyze_sentiment(text: str = Form(...)):
    """
    Analyze sentiment of input text using Mistral model.
    
    Args:
        text: The text to analyze for sentiment
        
    Returns:
        SentimentResponse with sentiment classification (Positive/Negative/Neutral)
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    
    if len(text) > 5000:
        raise HTTPException(status_code=400, detail="Text input exceeds maximum length of 5000 characters")
    
    import time
    start_time = time.time()
    
    try:
        prompt = (
            "What is the sentiment of this text? "
            "Respond with ONLY one of these exact words: Positive, Negative, or Neutral\n\n"
            f"Text: {text}\n\n"
            "Sentiment:"
        )
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_predict": 10
                }
            },
            timeout=45 #increased due to timeout errors
        )
        
        response.raise_for_status()
        result = response.json()
        
        sentiment = result.get("response", "").strip()
        
        # Normalize sentiment response
        valid_sentiments = ["Positive", "Negative", "Neutral"]
        sentiment = next((s for s in valid_sentiments if s.lower() in sentiment.lower()), "Neutral")
        
        processing_time = time.time() - start_time
        
        return SentimentResponse(
            sentiment=sentiment,
            processing_time=round(processing_time, 3)
        )
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request timeout - Ollama service took too long to respond")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama service")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.get("/models")
async def list_models():
    """List available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        return {"models": [model["name"] for model in models]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
