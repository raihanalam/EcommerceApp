
from django.urls import path
from . import views

app_name = 'Account_App'

urlpatterns = [
     path('signup/', views.sign_up, name="signup"),
     path('signin/', views.sign_in, name="signin"),
     path('signout/', views.sign_out, name="signout"),
     path('profile/', views.user_profile, name="profile"),
]