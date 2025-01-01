from django import forms

class SearchByNameOrDescriptionForm(forms.Form):
    keywords = forms.CharField(max_length=100,
                               label='Palabras clave',
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Introduce palabras clave'}))