from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'source', 'buying_price', 'manufacture_price','category',
            'selling_price', 'min_selling_price', 'sku', 'specifications',
            'stock', 'image'
        ]


class StockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
