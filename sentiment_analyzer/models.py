from django.db import models
from django.utils import timezone


class SentimentAnalysis(models.Model):
    text = models.TextField()
    polarity = models.FloatField()  # Range from -1 (negative) to 1 (positive)
    subjectivity = models.FloatField()  # Range from 0 (objective) to 1 (subjective)
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral
    created_at = models.DateTimeField(default=timezone.now)
    source_url = models.URLField(null=True, blank=True)  # For social media links

    def __str__(self):
        return f"{self.sentiment} ({self.polarity:.2f}) - {self.text[:50]}..."

    class Meta:
        ordering = ['-created_at']