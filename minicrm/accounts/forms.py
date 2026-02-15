from django import forms
from django.contrib.auth.models import User
from accounts.models import Company, CompanyUser,ROLE_CHOICES
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your desired username',
                'title': 'Your unique username',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'e.g., user@example.com'
            }),
        }

        help_texts = {
            'username': '',
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class StartCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'phone', 'industry']

class JoinCompanyForm(forms.Form):
    email = forms.EmailField(disabled=True)
    company_name = forms.CharField(max_length=255)



class AdminAddUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'username'}),
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'off', 'placeholder': 'email@example.com'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        label="Password"
    )

    company = forms.ModelChoiceField(queryset=Company.objects.all(), label="Company")
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    salary = forms.DecimalField(initial=0.00, required=False, label="Salary")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CompanyUserForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = ['role', 'salary', 'status']
