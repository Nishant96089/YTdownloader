from django import forms

class URLForm(forms.Form):
    video_url = forms.URLField(
        label='',
        max_length=200,
        widget=forms.URLInput(attrs={
            'placeholder': 'Paste your video link here',
            'class': 'form-control',
        })
    )
