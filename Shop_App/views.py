from django.shortcuts import render

#Import views
from django.views.generic import ListView, DetailView

#Models
from .models import Product, Category


# Create your views here.
'''
class Home(ListView):

     model = Product
     template_name = 'Shop_App/home.html'
'''

def home(request):
     categories = Category.objects.all().order_by('title')
     products = Product.objects.all()

     return render(request, 'Shop_App/home.html',context={ 'categories_list':categories, 'product_list':products })
     

class ProductDetail(DetailView):
     model = Product
     template_name = 'Shop_App/product_detail.html'