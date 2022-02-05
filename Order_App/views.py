import re
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from Order_App.models import Cart, Order
from Shop_App.models import Product

from django.contrib import messages

# Create your views here.

@login_required
def add_to_cart(request, pk):
     item = get_object_or_404(Product, pk=pk)
     order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased = False)
     order_qs = Order.objects.filter(user=request.user, ordered=False)

     if order_qs.exists():
          order = order_qs[0]
          if order.orderitems.filter(item=item).exists():
               order_item[0].quantity += 1
               order_item[0].save()
               messages.info(request, "This item quantity is updated.")
               return redirect("Shop_App:home")
          else:
               order.orderitems.add(order_item[0])
               messages.info(request,"This item is aded to your cart.")
               return redirect("Shop_App:home")
     else:
          order = Order(user=request.user)
          order.save()
          order.orderitems.add(order_item[0])
          messages.info(request,"This item is added to your cart.")
          return redirect("Shop_App:home")

@login_required
def cart_view(request):
     carts = Cart.objects.filter(user = request.user, purchased = False)
     orders = Order.objects.filter(user= request.user, ordered = False)

     if carts.exists() and orders.exists():
          order = orders[0]

          return render(request,'Order_App/cart.html', context={'carts':carts, 'order':order})
     else:
          messages.warning(request,'Your cart is empty. Please add some item!')
          return redirect('Shop_App:home')

@login_required
def remove_from_cart(request, pk):
     item = get_object_or_404(Product,pk=pk)
     order_qs = Order.objects.filter(user = request.user, ordered = False)
     if order_qs.exists():
          order = order_qs[0]
          if order.orderitems.filter(item=item).exists():
               order_item = Cart.objects.filter(item=item, user = request.user, purchased = False)[0]
               #order_item = order_item[0]
               order.orderitems.remove(order_item)
               order_item.delete()
               messages.warning(request, 'This item was removed.')
               return redirect('Order_App:cart')
          else:
               messages.info(request, 'This item was not in your cart.')
               return redirect('Shop_App:home')

     else:
          messages.info(request,"You don't have an active order.")
          return redirect('Shop_App:home')

@login_required
def increase_item(request,pk):
     item = get_object_or_404(Product,pk=pk)
     order_qs = Order.objects.filter(user=request.user , ordered = False)
     if order_qs.exists():
          order = order_qs[0]
          if order.orderitems.filter(item=item).exists():
               order_item = Cart.objects.filter(item=item,user=request.user, purchased = False)[0]
               if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.success(request,f"{item.name} quantity has been increased.")
                    return redirect('Order_App:cart')
          else:
               messages.info(request, f"{item.name} is not in your cart.")
     else:
          messages.info(request,"You dont have any active order")
          return redirect('Shop_App:home')

@login_required
def decrease_item(request,pk):
     item = get_object_or_404(Product,pk=pk)
     order_qs = Order.objects.filter(user=request.user, ordered = False)

     if order_qs.exists():
          order = order_qs[0]
          if order.orderitems.filter(item=item).exists():
               order_item = Cart.objects.filter(item=item, user=request.user, purchased = False)[0]
               if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.warning(request,f"{item.name} quantity has been decreased.")
                    return redirect('Order_App:cart')
               else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request,f"{item.name} has been removed from your cart.")
                    return redirect('Order_App:cart')
          else:
               messages.info(request, f"{item.name} is not in your cart.")
     else:
          messages.info(request,"You dont have any active order")
          return redirect('Shop_App:home')
