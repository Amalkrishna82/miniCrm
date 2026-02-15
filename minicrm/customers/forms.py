from django import forms
from customers.models import Customer,Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'status', 'assigned_to', 'address']

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','email','phone','address']
