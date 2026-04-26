"""
Frontend Application for Sentiment Analyzer.

This Streamlit app provides a user interface for analyzing text sentiment.
Users enter text and receive a classification (Positive, Negative, or Neutral)
from the Mistral model via the FastAPI backend.
"""

import os
import sys

import streamlit as st
import requests

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from components import render_app_footer, run_with_status_updates

# Set the main title of the Streamlit app
st.title("Sentiment Analyzer (Mistral)")

# Create a text area for user input
# This is where users enter the text they want analyzed
text_input = st.text_area("Enter your sentence here:")

# Check if the user clicked the "Analyze" button
if st.button("Analyze"):
    # Send the text to the backend API for sentiment analysis
    # The backend will use Mistral to determine sentiment
    response = run_with_status_updates(
        lambda: requests.post(
            "http://localhost:8000/analyze/",
            data={"text": text_input}
        ),
        start_message="Analyzing sentiment..."
    )

    # Extract the sentiment result from the JSON response
    # Fallback to "Error" if the response doesn't contain expected data
    sentiment = response.json().get("sentiment", "Error")

    # Display the predicted sentiment with a subheader
    st.subheader("Predicted Sentiment:")

    # Show the sentiment classification result
    st.write(sentiment)


render_app_footer()
