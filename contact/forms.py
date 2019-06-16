from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={
            'class': 'form-control',  # specify CSS class
            'placeholder': 'Your name'  # default text
        }
    ))
    email = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            'class': 'form-control',  # specify CSS class
            'placeholder': 'Your email address'  # default text
        }
    ))
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control'
        }
    ))
