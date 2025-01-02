from django import forms

class SearchByNameOrDescriptionForm(forms.Form):
    keywords = forms.CharField(max_length=100,
                               label='Palabras clave',
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Introduce palabras clave'}))
    
class SearchByPriceForm(forms.Form):
    lower_price = forms.FloatField(label='Precio mínimo (€)',
                                   required=False,
                                   widget=forms.NumberInput(attrs={'placeholder':'0'}))
    higher_price = forms.FloatField(label='Precio máximo (€)',
                                   required=False,
                                   widget=forms.NumberInput(attrs={'placeholder':'100'}))