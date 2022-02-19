from unicodedata import name
from django.urls import path
from . import views


app_name = 'Search_App'

urlpatterns = [
     path('', views.search , name='search' ),
     path('filter/', views.filter , name='filter' ),
]