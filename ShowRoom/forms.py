from django.forms import ModelForm
from django import forms
from .models import *


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        exclude = [ 'photo']

class BrandTitlePhotoForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['photo']

class MobileForm(ModelForm):
    class Meta:
        model = Mobile
        exclude = [ 'photo']

class MobileTitlePhotoForm(ModelForm):
    class Meta:
        model = Mobile
        fields = ['photo']

class MobilePhotoForm(ModelForm):
    class Meta:
        model = MobilePhoto
        fields = ['photo']

class UserForm(ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        exclude = ['userType','status']

class AdminForm(ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = '__all__'





# class CarAddForm(ModelForm):
#     class Meta:
#         model = Car
#         fields = '__all__'

# class CompanyAddForm(ModelForm):
#     class Meta:
#         model = Company
#         exclude = [ 'photo']

# class CompanyAddPhotoForm(ModelForm):
#     class Meta:
#         model = Company
#         fields = ['photo']

# class CarAddPhotoForm(ModelForm):
#     class Meta:
#         model = CarPhoto
#         fields = ['photo']