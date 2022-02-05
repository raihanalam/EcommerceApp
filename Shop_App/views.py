from re import template
from django.shortcuts import render

#Import views
from django.views.generic import ListView, DetailView

#Models
from .models import Product


# Create your views here.
class Home(ListView):

     model = Product
     template_name = 'Shop_App/home.html'


class ProductDetail(DetailView):
     model = Product
     template_name = 'Shop_App/product_detail.html'