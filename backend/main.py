"""
Backend API for Sentiment Analyzer using Mistral via Ollama.

This FastAPI application provides an endpoint that analyzes the sentiment
of text input (Positive, Negative, or Neutral) using a locally-hosted
Mistral model via Ollama.
"""
#Imports request and fastAPI modules
from fastapi import FastAPI, Form
import requests
import json

#
app = FastAPI()
OLLAMA_TIMEOUT_SECONDS = 1800

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def read_ollama_stream(response: requests.Response) -> str:
    """Read Ollama's streamed NDJSON chunks into one response string."""
    chunks = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        chunks.append(data.get("response", ""))
        if data.get("done"):
            break
    return "".join(chunks).strip()


def call_ollama(payload: dict) -> str:
    """Call Ollama with streaming enabled so long local generations stay alive."""
    streamed_payload = {**payload, "stream": True}
    with requests.post(
        OLLAMA_API_URL,
        json=streamed_payload,
        timeout=(10, OLLAMA_TIMEOUT_SECONDS),
        stream=True,
    ) as response:
        response.raise_for_status()
        return read_ollama_stream(response)

@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    """
    Analyze the sentiment of the provided text.

    Args:
        text: The input text to analyze (from HTML form data)

    Returns:
        A dictionary containing the sentiment classification
    """
    # Construct a prompt that explicitly asks for sentiment classification
    # The model is instructed to respond with only Positive, Negative, or Neutral
    # This constrained output format makes parsing the response straightforward
    prompt = (
        "What is the sentiment of this text? "
        "Respond with Positive, Negative, or Neutral:\n\n"
        f"{text}"
    )

    # Send the sentiment analysis request to Ollama's local API.
    # The helper streams chunks from Ollama, then returns one complete string.
    result = call_ollama({
        "model": "mistral",  # Using mistral for sentiment analysis
        "prompt": prompt,     # The formatted prompt with text to analyze
    })

    # Return the sentiment classification.
    return {"sentiment": result}
