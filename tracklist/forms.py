from django import forms


class TracklistForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',  # specify CSS class
            'placeholder': 'Podcast URL'  # default text
        }
    ))
