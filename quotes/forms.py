from django import forms 
from .models import Stock 

class StockFrom(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker']