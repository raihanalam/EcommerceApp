from django.shortcuts import render
from Shop_App.models import Category, Product

# Create your views here.
def search(request):
     if request.method == 'GET':
          search = request.GET.get('search','')
          result = Product.objects.filter(name__icontains = search )

     return render(request,'Search_App/result.html',context={'search': search, 'result':result})

def filter(request):
     try:
          if request.method == 'GET':
               filter = request.GET.get('category', '')
               f_category = Category.objects.get(title = filter)
               result = Product.objects.filter(category = f_category )

          return render(request,'Search_App/result.html',context={'filter': filter, 'result':result})
     except:
          return render(request,'Search_App/result.html',context={'filter': filter})
          
