from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .forms import TextAnalysisForm
from .models import SentimentAnalysis
from .sentiment_utils import (
    analyze_sentiment,
    extract_text_from_url,
    generate_sentiment_visualization,
    generate_sentiment_donut_chart
)


def analyze_text_view(request):
    form = TextAnalysisForm()
    analysis_result = None

    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            url = form.cleaned_data.get('url')

            if url and not text:
                text = extract_text_from_url(url)

            if text:
                # Analyze sentiment
                result = analyze_sentiment(text)

                # Save to database
                analysis = SentimentAnalysis(
                    text=text,
                    polarity=result['polarity'],
                    subjectivity=result['subjectivity'],
                    sentiment=result['sentiment'],
                    source_url=url if url else None
                )
                analysis.save()

                # Add text to the result
                result['text'] = text
                analysis_result = result

    # Get all previous analyses for visualization
    previous_analyses = SentimentAnalysis.objects.order_by('-created_at')[:20]
    line_chart = generate_sentiment_visualization(previous_analyses)
    donut_chart = generate_sentiment_donut_chart(previous_analyses)

    context = {
        'form': form,
        'result': analysis_result,
        'previous_analyses': previous_analyses,
        'line_chart': line_chart,
        'donut_chart': donut_chart
    }

    return render(request, 'sentiment_analyzer/analyze.html', context)


class AnalysisHistoryView(ListView):
    model = SentimentAnalysis
    template_name = 'sentiment_analyzer/history.html'
    context_object_name = 'analyses'
    paginate_by = 10


class AnalysisDetailView(DetailView):
    model = SentimentAnalysis
    template_name = 'sentiment_analyzer/detail.html'
    context_object_name = 'analysis'