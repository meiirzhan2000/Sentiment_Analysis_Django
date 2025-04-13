from django.test import TestCase
from django.urls import reverse
from .models import SentimentAnalysis
from .sentiment_utils import analyze_sentiment


class SentimentAnalysisTests(TestCase):
    def test_sentiment_analysis_positive(self):
        """Test that positive text is classified correctly."""
        text = "I love this product! It's amazing and works perfectly."
        result = analyze_sentiment(text)
        self.assertEqual(result['sentiment'], 'Positive')
        self.assertTrue(result['polarity'] > 0)

    def test_sentiment_analysis_negative(self):
        """Test that negative text is classified correctly."""
        text = "This is terrible. I hate how poorly it works."
        result = analyze_sentiment(text)
        self.assertEqual(result['sentiment'], 'Negative')
        self.assertTrue(result['polarity'] < 0)

    def test_sentiment_analysis_neutral(self):
        """Test that neutral text is classified correctly."""
        text = "This is a factual statement. The sky exists. Today is a day."
        result = analyze_sentiment(text)
        self.assertEqual(result['sentiment'], 'Neutral')
        self.assertTrue(-0.1 <= result['polarity'] <= 0.1)

    def test_analyze_view(self):
        """Test that the analyze view works correctly."""
        response = self.client.get(reverse('sentiment_analyzer:analyze'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sentiment_analyzer/analyze.html')

        # Test posting text for analysis
        post_data = {'text': 'This is a test. I am happy.', 'url': ''}
        response = self.client.post(reverse('sentiment_analyzer:analyze'), post_data)
        self.assertEqual(response.status_code, 200)

        # Check that an analysis was created in the database
        self.assertEqual(SentimentAnalysis.objects.count(), 1)
        analysis = SentimentAnalysis.objects.first()
        self.assertEqual(analysis.text, 'This is a test. I am happy.')
        self.assertEqual(analysis.sentiment, 'Positive')