from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#For canceling CSRF Checking
from django.views.decorators.csrf import csrf_exempt

#Models and Forms
from Order_App.models import Cart, Order
from .models import BillingAddress
from .forms import BillingForm
import socket

# For API
import requests

#Payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

# Create your views here.
@login_required
def checkout(request):
     saved_address = BillingAddress.objects.get_or_create(user = request.user )
     saved_address = saved_address[0]
     form = BillingForm(instance=saved_address)
     if request.method == "POST":
          form = BillingForm(request.POST, instance=saved_address)
          if form.is_valid():
               form.save()
               form = BillingForm(instance=saved_address)
               messages.success(request, 'Shipping address Saved!')
     order_qs = Order.objects.filter(user = request.user , ordered =False)
     #print(order_qs)
     order_items = order_qs[0].orderitems.all()
     #print(order_items)
     order_total = order_qs[0].get_totals()
     #print(order_total)

     return render(request, 'Payment_App/checkout.html', context={'form':form, 'order_items':order_items, 'order_total':order_total, 'saved_address':saved_address})



@login_required
def payment(request):
     saved_address = BillingAddress.objects.get_or_create(user=request.user)
     saved_address =saved_address[0]
     if not saved_address.is_fully_filled():
          messages.info(request,f"Please complete shipping address!")
          return redirect("Payment_App:checkout")

     if not request.user.profile.is_fully_filled():
          messages.info(request,f"Please complete all information of your profile.")
          return redirect('Account_App:profile')

     #SSLCommerz Store ID
     store_id = 'syste61fac7875d0bb'
     #API key
     store_pass = 'syste61fac7875d0bb@ssl'
     
     status_url = request.build_absolute_uri(reverse("Payment_App:complete"))

     mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id= store_id, sslc_store_pass=store_pass)
     mypayment.set_urls(success_url=  status_url, fail_url=  status_url, cancel_url=  status_url, ipn_url=  status_url)


     order_qs = Order.objects.filter(user=request.user, ordered = False)
     order_items = order_qs[0].orderitems.all()
     order_items_count = order_qs[0].orderitems.count()
     order_total = order_qs[0].get_totals()

     mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')


     current_user = request.user

     mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)
     mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)


     response_data = mypayment.init_payment()
     #print(response_data)
     return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
     if request.method == 'POST' or request.method == 'post':
          payment_data = request.POST
          #print(payment_data)

          status = payment_data['status']

          if status == 'VALID':
               val_id = payment_data['val_id']
               tran_id = payment_data['tran_id']
               bank_tran_id = payment_data['bank_tran_id']
               tran_date = payment_data['tran_date']
               payment_type = payment_data['card_type']

               messages.success(request,f'Your payment is successfully done by {payment_type}')
               #messages.info(request,f'Page will auto redirect to home after 5 seconds.')

               return HttpResponseRedirect(reverse('Payment_App:purchase', kwargs={'val_id':val_id, 'tran_id':tran_id}))

          elif status == 'FAILED':
               messages.warning(request,f'Your payment Failed! Please try again.')
               messages.info(request,f'Page will auto redirect to home after 5 seconds.')
               
          elif status == 'CANCELLED':
               messages.warning(request,f'OOPS! You canceled your payment, Please try again.')
               messages.info(request,f'Page will auto redirect to home after 5 seconds.')

     return render(request,'Payment_App/complete.html',context={})


@login_required
def purchase(request, val_id, tran_id):

     order_qs = Order.objects.filter(user=request.user, ordered = False)
     order = order_qs[0]
     orderId = tran_id
     order.ordered = True
     order.orderId = orderId
     order.paymentId = val_id
     order.save()
     cart_items = Cart.objects.filter(user=request.user, purchased= False)
     for item in cart_items:
          item.purchased = True
          item.save()
     
     return HttpResponseRedirect(reverse('Shop_App:home'))

@login_required
def orders(request):
     try:
          orders = Order.objects.filter(user=request.user, ordered=True)
          context = {"orders":orders}
     except:
          messages.warning(request, 'You don not have an active order.')
          return redirect("Shop_App:home")
     return render(request,"Payment_App/order.html",context)