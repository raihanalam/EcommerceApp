from django.urls import path
from . import views

app_name = 'Shop_App'

urlpatterns = [
     path('', views.home, name='home'),
     path('product/<pk>/',views.ProductDetail.as_view(), name='product_detail')
]
