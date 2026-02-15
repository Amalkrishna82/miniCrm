from django import forms
from transaction.models import Order, OrderItem, Service

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'selling_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ServiceForm(forms.ModelForm):
    SELECT_TYPE = (
        ('customer', 'Customer'),
        ('lead', 'Lead'),)
    select_type = forms.ChoiceField(choices=SELECT_TYPE,widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='customer')
    class Meta:
        model = Service
        fields = [
            'select_type','customer','lead','product','description','service_type','assigned_to','service_date','status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
