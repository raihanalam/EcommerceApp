from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from . models import User, Profile

from django.contrib.auth.forms import UserCreationForm



# forms
class ProfileForm(ModelForm):

     class Meta:
          model = Profile
          exclude = ('user',)

class SignUpForm(UserCreationForm):
     
     class Meta:
          model = User
          fields =('email','password1', 'password2')
