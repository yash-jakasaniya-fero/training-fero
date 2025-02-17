from django import forms
from .models import Product, Manufacturer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'