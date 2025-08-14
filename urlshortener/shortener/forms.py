from django import forms

class URLForm(forms.Form):
    original_url = forms.URLField(label='Enter URL to shorten', widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://example.com',
    }))