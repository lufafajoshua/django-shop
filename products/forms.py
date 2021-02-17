from django import forms
from .models import Category, Product

class SearchForm(forms.Form):
    choices = (('Product', 'Product'), ('Category', 'Category'))
    select = forms.CharField(widget=forms.Select(choices=choices))
    search_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-name', 'name':'form-name', 'placeholder':'Search products...'}))
