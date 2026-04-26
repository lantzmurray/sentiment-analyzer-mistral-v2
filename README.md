# Project 2: Sentiment Analyzer (Mistral)

An AI-powered sentiment analysis application that classifies text sentiment as Positive, Negative, or Neutral. Perfect for social media monitoring, customer feedback analysis, and text mining.

## Features

- **Sentiment Classification**: Identifies emotional tone (Positive, Negative, Neutral)
- **Confidence Scoring**: Provides confidence levels for each classification
- **Batch Processing**: Analyze multiple texts at once
- **FastAPI Backend**: Efficient REST API for processing
- **Streamlit Frontend**: User-friendly interface for text input
- **Local Processing**: All analysis runs locally using Ollama LLMs - no external API dependencies

## Architecture

### Backend Components

1. **Sentiment Analyzer** (`backend/main.py`)
   - Classifies text sentiment
   - Provides confidence scores
   - Handles multiple texts efficiently

### Frontend Components

1. **Streamlit UI** (`frontend/app.py`)
   - User interface for text input
   - Results display and visualization
   - Export functionality

2. **Reusable Components** (`frontend/components.py`)
   - Modular UI elements
   - Consistent styling and layout

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-02-sentiment-analyzer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (mistral is recommended)
   ollama pull mistral
   # Start Ollama service
   ollama serve
   ```

## Running the Application

### Backend API

1. **Start the FastAPI backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Access the API**: Navigate to `http://localhost:8000` for API documentation

### Frontend UI

1. **Start the Streamlit application** (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Input Text

- Paste text in the text area
- Or upload a text file with multiple texts
- Enter one text per line for batch processing

### 2. Analyze Sentiment

- Click "Analyze" to process the text
- Wait for the AI to classify sentiment
- View the comprehensive results

### 3. Review Results

- **Sentiment**: Positive, Negative, or Neutral classification
- **Confidence**: AI confidence level in the classification
- **Statistics**: Overall sentiment distribution
- **Individual Results**: Detailed analysis for each text

### 4. Export Results

- Copy results for reports
- Export analysis as CSV or JSON
- Save for future reference

## Workflow

```
Input Text → Backend API → Ollama LLM → Classify Sentiment → Display Results
     ↓               ↓            ↓                ↓                  ↓
  Paste text     FastAPI      Call model      Classify      Show to
  or file        endpoint     as Positive/    user
                                   Negative
                                   Neutral
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=mistral
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `mistral` - Lightweight and efficient for sentiment analysis (default)

## Project Structure

```
soai-02-sentiment-analyzer/
├── backend/
│   └── main.py                  # FastAPI backend
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── requirements.txt              # Python dependencies
└── README.md                   # This file
```

## Dependencies

- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `streamlit` - Web UI framework
- `requests` - HTTP client for Ollama API
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull mistral`

### Backend API Issues

If the backend isn't responding:
1. Verify uvicorn is running: `ps aux | grep uvicorn`
2. Check the port isn't in use: `lsof -i :8000`
3. Review backend logs for errors

### Frontend Connection Issues

If the frontend can't connect to the backend:
1. Verify both services are running
2. Check the API URL in frontend/app.py
3. Ensure CORS is configured correctly

### Analysis Issues

If sentiment classification isn't working:
1. Check that text is properly formatted
2. Verify the LLM model is appropriate
3. Review the prompts in backend/main.py
4. Try with a different model

### Slow Performance

For faster analysis:
1. Use mistral for speed
2. Reduce the number of texts
3. Increase Ollama's GPU resources if available

## Use Cases

- **Social Media Monitoring**: Track sentiment trends over time
- **Customer Feedback**: Analyze customer reviews and feedback
- **Text Mining**: Extract sentiment from large text datasets
- **Market Research**: Analyze public sentiment data
- **Brand Monitoring**: Track brand mentions and sentiment
- **Content Moderation**: Filter inappropriate content

## Important Notes

- All processing happens locally - no data is sent to external servers
- Sentiment classification is AI-based and should be verified
- Mistral is optimized for text analysis tasks
- Confidence scores indicate AI certainty in classification
- This tool provides analysis but not business advice

## License

This project is part of the School of AI curriculum.
