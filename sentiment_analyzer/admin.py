from django.contrib import admin
from .models import SentimentAnalysis


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('sentiment', 'polarity', 'subjectivity', 'truncated_text', 'created_at')
    list_filter = ('sentiment', 'created_at')
    search_fields = ('text', 'source_url')
    readonly_fields = ('polarity', 'subjectivity', 'sentiment', 'created_at')
    date_hierarchy = 'created_at'

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Text'