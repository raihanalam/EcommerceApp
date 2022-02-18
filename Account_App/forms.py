import email
from django import forms
from django.forms import ModelForm
from . models import User, Profile

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# forms
class ProfileForm(ModelForm):

     class Meta:
          model = Profile
          exclude = ('user',)

class SignUpForm(UserCreationForm):
     email = forms.EmailField(required=True,label="",widget=forms.EmailInput(attrs={'placeholder':'Email'}))
     password1 = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
     password2 = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
     class Meta:
          model = User
          fields =('email','password1', 'password2')

class SignInForm(AuthenticationForm):
     username = forms.EmailField(required=True,label="",widget=forms.EmailInput(attrs={'placeholder':'Email'}))
     password = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

     class Meta:
          model = User
          fields =('email','password')
