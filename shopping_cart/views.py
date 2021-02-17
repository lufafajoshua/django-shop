from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
#from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from user_profiles.models import Profile
from products.models import Product

from shopping_cart.extras import generate_order_id, transact, generate_client_token
from shopping_cart.models import OrderItem, Order, Transaction, ShippingInfo

import datetime
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid

# stripe.api_key = settings.STRIPE_SECRET_KEY
from .forms import PaymentForm

import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid
from base64 import b64encode


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()#retrieve specific objects by their id we are to add products by their id
    # check if the user already owns this product
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('products:product_list')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product, price=product.price)#Add the quantity when needed ie quantity=form.get['quantity]
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('products:product_list'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))

@login_required()
def order_details(request, **kwargs):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            update_item(request)

    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)

    # @login_required()
    # def process_payment(request, **kwargs):
    #     existing_order = get_user_pending_order(request)
    #     order_id = existing_order.id
    #     order = existing_order
    #     host = request.get_host
        
    #     paypal_dict = {
    #         'business': settings.PAYPAL_RECEIVER_EMAIL,
    #         'amount': '%.2f' % order.get_cart_total().quantize(
    #             Decimal('.01')),
    #         'item_name': 'Order {}'.format(order.id),
    #         'invoice': str(order.id),
    #         'currency_code': 'USD',
    #         'notify_url': 'http://{}{}'.format(host,
    #                                         reverse('paypal-ipn')),
    #         'return_url': 'http://{}{}'.format(host,
    #                                         reverse('shopping_cart:payment_done')),#args=(existing_order.id,)
    #         'cancel_return': 'http://{}{}'.format(host,
    #                                             reverse('shopping_cart:payment_cancelled')),                                      
    #     }
    #     form = PayPalPaymentsForm(initial=paypal_dict)
    
    context = {
        'form': form,
        'order': existing_order,
    }
    return render(request, 'shopping_cart/process_payment.html', context)

def get_auth_token(): 
    api_user = 'de2aea87-fdd1-432a-8d21-7e488fb1ee49'
    api_key = '002c242c2aa047b7926c3d86dbf1b9a5' 
    api_user_and_key  = api_user+':'+api_key
    api_user_and_key_bytes = base64.b64encode(api_user_and_key.encode()).decode()

    headers = {
        # Request headers
        'Authorization': "Basic "+api_user_and_key_bytes,
        #'Authorization': 'Basic' +api_user_and_key_bytes,
        
            # 'X-Callback-Url': '',
            # 'X-Reference-Id': '6cb5711b-5d29-4053-aaa1-516ec394f044',
        #'X-Target-Environment': 'oauth2',
        #'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
    }
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')#replace with ericssonbasicapi2.azure-api.net when having a new connection
        conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        print(response.status)
        print(response.reason)
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}]".format(e))  

@login_required()
def make_payment(request, **kwargs):
    existing_order = get_user_pending_order(request)
    total_amount = existing_order.get_cart_total()    
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6ImRlMmFlYTg3LWZkZDEtNDMyYS04ZDIxLTdlNDg4ZmIxZWU0OSIsImV4cGlyZXMiOiIyMDIxLTAyLTE3VDA5OjQ4OjA5LjY1NCIsInNlc3Npb25JZCI6ImM3OTNjZmFkLWMyNTQtNGQ0Zi1hODllLTE1ZDYzYjA0Y2Q0OCJ9.Vctj4LT6HZKzxNKP44xlMN33PA1AJOCdJPz2ji0s62qRzu7jVjsoPprLOnnUcrv-mgkzmVMLSEoXdh3LP_iP5BQajw3oyRQdTxzzVb-jE78Ms1IFTlmEhTa1s_ymC9xoSDkrYmXZXrWm9FRlKo17rNbCRMh9QZdewDfEX6hiLaPRqzXlJrImjQJlfQ2Jj8JLqWRVtFbe93HHmH0uyerNwIhBuUuhcQ28PvbScT7s4qeaYb7_nDKr8sUVfKqMBs50Zx30fnJ1FMdAAv8hNvEVJ9eVYP40YVzN7Yplq2_SJAg3a_7lmf0Vc2FU-JsWExlBLi0MnJtCTOOp5xv8ELbVNw"
    #token = get_auth_token()#Try using the function with internet to check whether its working
    reference_id = str(uuid.uuid4())

    form = PaymentForm(request.POST)
   
    if form.is_valid():
        phone = form.cleaned_data['phone_no']
        headers = {
            # Request headers
            'Authorization': 'Bearer '+token,
            #'X-Callback-Url': 'https://winnershield.com',#Point to the transaction urls so to create the transaction information
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'sandbox',
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
        }

        params = urllib.parse.urlencode({
        })

        body = json.dumps({
        "amount": str(total_amount),#Turn this to string in case of errors
        "currency": "EUR",
        "externalId": "12345",
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone,#Get this from the frontend
        },
        "payerMessage": "Successfully Paid",
        "payeeNote": "Hello Successfull"
        })

        try:
            conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
            conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            print(response.status)
            conn.close()
            ship_info = ShippingInfo(
                #email=form.address.cleaned_data['email'],
                address=form.cleaned_data['address'],
                telephone=phone,
                order=existing_order
            )
            ship_info.save()#Create the shipinfo for a specific order
            if response.status == 202:#Check for what returns a successful payment
                #return redirect(reverse('shopping_cart:payment_done', args=(existing_order.id,)))#Try using the token and see the results
                return redirect(reverse('shopping_cart:update_records', args=(existing_order.id,)))#args=(existing_order.id,) 
        except Exception as e:
            print("[Errno {0}]".format(e))
        finally:
            print("Transaction in Progress")    
    context = {
        'order': existing_order,
        'form': form,
    }    
    return render(request, 'shopping_cart/mtnmomo.html', context)    

def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    # publishKey = settings.STRIPE_PUBLISHABLE_KEY
    # if request.method == 'POST':
    #     token = request.POST.get('stripeToken', False)#payments with stripe
    #     if token:
    #         try:
    #             charge = stripe.Charge.create(
    #                 amount=100*existing_order.get_cart_total(),
    #                 currency='usd',
    #                 description='Example charge',
    #                 source=token,
    #             )

    #             return redirect(reverse('shopping_cart:update_records',
    #                     kwargs={
    #                         'token': token
    #                     })
    #                 )
    #         except stripe.CardError as e:
    #             message.info(request, "Your card has been declined.")
    #     else:#payments with braintree 
    #         result = transact({
    #             'amount': existing_order.get_cart_total(),
    #             'payment_method_nonce': request.POST['payment_method_nonce'],
    #             'options': {
    #                 "submit_for_settlement": True
    #             }
    #         })

    #         if result.is_success or result.transaction:
    #             return redirect(reverse('shopping_cart:update_records',
    #                     kwargs={
    #                         'token': result.transaction.id
    #                     })
    #                 )
    #         else:
    #             for x in result.errors.deep_errors:
    #                 messages.info(request, x)
    #             return redirect(reverse('shopping_cart:checkout'))
            
    context = {
        'order': existing_order,
            # 'client_token': client_token,
            # 'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'shopping_cart/checkout.html', context)

@login_required()
@csrf_exempt
def payment_done(request, order_id):#def payment_done(request, order_id):
        # get the order being processed
    order_to_purchase = get_user_pending_order(request)#order_to_purchase = get_user_pending_order(request, id=order_id)
    
    # update the placed order which calls the UPDATE SQL command in the backend
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items using the update() method   
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()
    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()
    """ Clear the cart after a successfull transaction """
    order_to_purchase.items.delete()#Delete the order items after the payment is done form the cart

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return render(request, 'shopping_cart/payment_done.html')

@login_required()
@csrf_exempt
def payment_canceled(request):
    return render(request, 'shopping_cart/payment_cancelled.html')

@login_required()
def update_transaction_records(request, order_id):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)
    print(order_to_purchase)
    # update the placed order which calls the UPDATE SQL command in the backend
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items using the update() method   
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()
    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()
    
    #order_to_purchase.items.clear()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('products:product_list'))#return a redirect to the users profile with their products they have purchased

def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})

@login_required()
def update_item(request, **kwargs):
    """Get the order and then update the quantity of products"""
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    order_item = get_object_or_404(OrderItem, id=item_id)
    if quantity.isdigit():
        quantity = int(quantity)
        order_item.quantity = quantity
        order_item.save()

"""
PAyments with Mtn Momo API
"""
reference_id = str(uuid.uuid4())
headers = {
    # Request headers
    'Authorization': '',
    'X-Callback-Url': '',
    #'X-Reference-Id': 'reference_id',
    'X-Target-Environment': '',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ee930ca35de2454990f001b023ded0e2',
}

params = urllib.parse.urlencode({
})

body = json.dumps({
  "providerCallbackHost": "" })

try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", "/v1_0/apiuser/169d38b5-98d3-48ac-aafd-0827d4d8f2db/apikey?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] ".format(e))

@login_required()
def sold_orders(request, **kwargs):
    #Get all the sold orders, from the sold orders get the sold products
    sold_orders = Order.objects.filter(is_ordered=True)
    products = []#list to hold the yilded products
    def products():    
        for order in sold_orders:
            for item in order.items.all():
                    # products.append(item)
                    # print(products)
                yield item
    sold_products = list(products())  
    print(sold_products)      
    context = {
        'sold_orders': sold_orders,
        'products': sold_products,
    }
    return render(request, 'shopping_cart/sold.html', context)

@login_required()
def sold_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'shopping_cart/sold_order.html', context)

""" Get all orders that have been paid and belong to a particular user"""
def my_orders(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    orders = Order.objects.filter(owner=user_profile, is_ordered=True)
    print(orders)
        # if order.exists():
        #     # get the only order in the list of filtered orders
        #     return order[0]
        # return 0
    context ={
        'my_orders': orders
    }    
    return render(request, 'shopping_cart/profile.html', context)