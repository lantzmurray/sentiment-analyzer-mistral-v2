import streamlit as st
import requests
import time
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sentiment-positive {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f44336;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000"

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Call backend API to analyze sentiment"""
    try:
        response = requests.post(
            f"{API_URL}/analyze/",
            data={"text": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to the backend. Make sure the API is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def get_sentiment_emoji(sentiment: str) -> str:
    """Return emoji based on sentiment"""
    emoji_map = {
        "Positive": "😊",
        "Negative": "😞",
        "Neutral": "😐"
    }
    return emoji_map.get(sentiment, "❓")

def get_sentiment_color(sentiment: str) -> str:
    """Return CSS class based on sentiment"""
    color_map = {
        "Positive": "sentiment-positive",
        "Negative": "sentiment-negative",
        "Neutral": "sentiment-neutral"
    }
    return color_map.get(sentiment, "")

# Main application
def main():
    st.title("🎭 Sentiment Analyzer")
    st.markdown("### AI-Powered Text Sentiment Analysis using Mistral")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        st.info("Make sure Ollama is running with the Mistral model:")
        st.code("ollama pull mistral\nollama serve", language="bash")
        st.markdown("---")
        st.markdown("### API Status")
        try:
            health_response = requests.get(f"{API_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ Backend API is healthy")
            else:
                st.warning("⚠️ Backend API is degraded")
        except:
            st.error("❌ Backend API is not reachable")
    
    # Main content
    st.markdown("---")
    
    # Input section
    st.markdown("### 📝️ Enter Your Text")
    text_input = st.text_area(
        "Type or paste your text here:",
        placeholder="Example: I absolutely love this product! It's amazing and exceeded all my expectations.",
        height=150,
        max_chars=5000,
        help="Maximum 5000 characters"
    )
    
    # Character count
    if text_input:
        char_count = len(text_input)
        st.caption(f"Characters: {char_count}/5000")
        if char_count > 5000:
            st.warning("⚠️ Text exceeds maximum length")
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Sentiment",
            use_container_width=True,
            disabled=not text_input or len(text_input) > 5000
        )
    
    # Results section
    if analyze_button and text_input:
        with st.spinner("🔄 Analyzing sentiment..."):
            result = analyze_sentiment(text_input)
        
        if result:
            sentiment = result.get("sentiment", "Neutral")
            processing_time = result.get("processing_time", 0)
            
            # Display result with styling
            emoji = get_sentiment_emoji(sentiment)
            css_class = get_sentiment_color(sentiment)
            
            st.markdown("---")
            st.markdown("### 📊 Analysis Result")
            
            # Sentiment card
            st.markdown(f"""
            <div class="{css_class}">
                <h2>{emoji} {sentiment}</h2>
                <p><strong>Processing Time:</strong> {processing_time:.3f} seconds</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional info
            with st.expander("📋 Details"):
                st.write(f"**Sentiment Classification:** {sentiment}")
                st.write(f"**Model Used:** Mistral (via Ollama)")
                st.write(f"**Text Length:** {len(text_input)} characters")
                st.write(f"**API Response Time:** {processing_time:.3f}s")
    
    # Sample texts for testing
    st.markdown("---")
    st.markdown("### 🧪 Try Sample Texts")
    
    sample_texts = {
        "Positive Example": "This is the best product I've ever used! The customer service was exceptional and the quality exceeded all my expectations.",
        "Negative Example": "I'm extremely disappointed with this purchase. The product arrived damaged and the support team was unhelpful and rude.",
        "Neutral Example": "The package arrived yesterday. It contains three items as described in the order confirmation."
    }
    
    for label, sample in sample_texts.items():
        if st.button(f"Use {label}", key=label):
            st.session_state.text_input = sample
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Built with ❤️ using Mistral, FastAPI, and Streamlit | School of AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
