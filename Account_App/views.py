from django.http import HttpResponse, request
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

#Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

#Form and models
from .models import Profile
from .forms import ProfileForm, SignInForm, SignUpForm

#Messages
from django.contrib import messages

# Create your views here.
def sign_up(request):
     form = SignUpForm()

     if request.method == 'POST':
          form = SignUpForm(request.POST)

          if form.is_valid():
               form.save()
               messages.success(request, "Account created successfully.")
               return HttpResponseRedirect(reverse('Account_App:signin'))
     return render(request,'Account_App/signup.html',context={'form':form})

def sign_in(request):

     form = SignInForm()

     if request.method == 'POST':
          form = SignInForm(data=request.POST)

          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username,password=password)

               if user is not None:
                    login(request,user)
                   
                    return HttpResponseRedirect(reverse('Shop_App:home'))

     return render(request,'Account_App/signin.html',context={'form':form})

@login_required
def sign_out(request):

     logout(request)
     messages.warning(request,"Successfully signed out!")
     return HttpResponseRedirect(reverse('Shop_App:home'))


@login_required
def user_profile(request):
     profile = Profile.objects.get(user=request.user)

     form = ProfileForm(instance=profile)

     if request.method == 'POST':
          form = ProfileForm(request.POST, instance=profile)

          if form.is_valid():
               form.save()
               messages.success(request,"Profile Upadated.")
               form = ProfileForm(instance=profile)
     
     return render(request,'Account_App/change_profile.html',context={ 'form':form })