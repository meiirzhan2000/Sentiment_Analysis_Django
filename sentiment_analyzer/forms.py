from django import forms


class TextAnalysisForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        required=False,
        label="Enter text to analyze"
    )
    url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label="Or enter a URL to analyze"
    )

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        url = cleaned_data.get('url')

        if not text and not url:
            raise forms.ValidationError("Please enter either text or a URL.")

        return cleaned_data