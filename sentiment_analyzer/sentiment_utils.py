import nltk
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend

# Download necessary NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def analyze_sentiment(text):
    """
    Analyze sentiment of text using TextBlob.
    Returns polarity, subjectivity, and sentiment label.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    # Determine sentiment label based on polarity
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment
    }


def extract_text_from_url(url):
    """
    Extract main text content from a URL.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text(separator=' ', strip=True)

        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def generate_sentiment_visualization(analyses):
    """
    Generate a visualization of sentiment analysis results over time.
    """
    if not analyses:
        return None

    # Create DataFrame for plotting
    df = pd.DataFrame([
        {
            'date': analysis.created_at,
            'polarity': analysis.polarity,
            'subjectivity': analysis.subjectivity,
            'sentiment': analysis.sentiment,
            'text': analysis.text[:50] + '...' if len(analysis.text) > 50 else analysis.text
        }
        for analysis in analyses
    ])

    # Create a simple line chart with Matplotlib (basic option)
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(df)), df['polarity'], marker='o', linestyle='-', color='blue', label='Polarity')
    plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    plt.xlabel('Analysis ID')
    plt.ylabel('Polarity Score')
    plt.title('Sentiment Polarity Over Time')
    plt.legend()
    plt.tight_layout()

    # Save to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the image to base64 string
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f'data:image/png;base64,{img_str}'


def generate_sentiment_donut_chart(analyses):
    """
    Generate a donut chart showing the distribution of sentiment categories.
    """
    if not analyses:
        return None

    # Count sentiments
    sentiment_counts = {}
    for analysis in analyses:
        sentiment = analysis.sentiment
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts[sentiment] = 1

    # Create donut chart with Matplotlib
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}

    # Use only available colors
    chart_colors = [colors.get(label, 'blue') for label in labels]

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=chart_colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.5))
    plt.axis('equal')
    plt.title('Sentiment Distribution')

    # Save to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the image to base64 string
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f'data:image/png;base64,{img_str}'