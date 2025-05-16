from django import forms
from django.forms import ModelForm
from .models import Transaction, Category, Budget, Alert
from django.contrib.auth.models import User


# ✅ User Registration Form
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


# ✅ Login Form (if used separately)
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# ✅ Transaction Form (for create)
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']

# ✅ Edit Transaction Form (for update)
class EditTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']


# ✅ Category Form
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']




# ✅ Admin User Form (Admin can manage users)
class AdminUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active', 'is_staff']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# ✅ Budget Form
class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']


# ✅ Alert Form (optional - usually alerts are generated automatically)
class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ['message', 'is_read']
