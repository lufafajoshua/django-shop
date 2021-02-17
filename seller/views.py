from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from .models import Seller
from products.models import Product
#from.forms import ProfileForm
from shopping_cart.models import Order
from shopping_cart.views import sold_orders
from collections import Counter
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
from .forms import SellerSignUpForm, LoginForm
from django.http import HttpResponseRedirect
from user_profiles.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
import datetime

def all_sellers(request):#Get all the sellers with the system
    sellers = Seller.objects.all()
    print(sellers)
    context = {
        'sellers': sellers,
    }
    return render(request, 'seller/sellers.html', context)

def sold_orders(request):
    sold_orders = Order.objects.filter(is_ordered=True)
    #get all the orderitems in the sold orders
    products = []#list to hold the yilded products
    for order in sold_orders:
        products = [item for item in order.items]
    return products    


def seller_profile(request):
    seller = get_object_or_404(Seller, user=request.user)  
    products = seller.product_set.all()
    context = {
        'seller': seller,
        'products': products,
    }
    return render(request, 'seller/profile.html', context)


def seller_detail(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)#Use filters to get the user type object and also the object id
    print(seller.user)
    #seller = get_object_or_404(Seller, pk=seller_id)
    products = seller.product_set.all()#Get all the products owned by a seller
    sold_orders = Order.objects.filter(is_ordered=True)
    #Get all the products in the sold orders
    def sold_products():    
        for order in sold_orders:
            for item in order.items.all():
                    # products.append(item)
                yield item
    sold_products = list(sold_products())  
    #print(sold_products) 
    def test():
        sold = []#This is a list to contain the products from the iteration or sold products
        quantity = []#A list ot hold tha various quantities of the products that were sold
        for product in products:
            for item in sold_products:
                total_quantity = 0
                if product == item.product:
                    sold.append(product.name)
                    quantity.append(item.quantity)
        merged = list(zip(sold, quantity))#Create a list with tuples containing the various sold products and their various quantities
        #print(list(merged)) 
        first = itemgetter(0)
        """two methods to summarize the """
        sums = [(k, sum(item[1] for item in tups))
            for k, tups in groupby(sorted(merged, key=first), key=first)]
        print(sums)
        d = defaultdict(int)
        for i,j in list(merged):
            d[i] += j
        s = list(zip(d.keys(),d.values())) 
        l = dict(s)#create a dictionary from the zipped and sorted or summed up list 
          
        #return the dictionary with the sold products and their respective quantities  
        """ returns a a dictionary containing the sold products and their quantities """                    
        return l
        
    sold_products = test()
    print(sold_products)

    context = {
        'seller': seller,
        'products': products,
        'sold': sold_products,#sold products belonging to a particular seller
    }
    return render(request, 'seller/seller_detail.html', context)

class SellerSignUpView(CreateView):
    model = User
    form_class = SellerSignUpForm
    template_name = 'registration/seller_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        #return HttpResponseRedirect(reverse('seller:seller_detail', args=[user.id],))
        return redirect('seller:login')#Redirect to the seller login to guide them to their accountspage where they can manage their information from



#login for he customer
def sellerlogin(request):
        # username = request.POST['username']
        # password = request.POST['password']
   
    msg = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.user_type == 2:
                    # Redirect to a success page.
                    return redirect('seller:seller_detail', args=(user.id,))
                elif user.user_type == 1:    
                    return redirect('products:product_list')
                elif user.user_type == 3:    
                    return redirect('django_chatter:chatroom')    
            else:
                msg = 'Invalid Username or Password'
    else:
        form = LoginForm()              
    context = {
        'msg': msg,
        'form': form,
    }    
    return render(request, 'registration/login.html', context)    


#def profile(request):#profile for the seller to check for their informaation about their products
    #get the products that a seller has with the system or company
    #get all the products that belong to a seller that have been sold in a given amount of time
    #Even calculate the total amount of money expected from the sold products
    pass    

    # def create_profile(request):
    #     if request.method == 'POST':
    #         form = ProfileForm(request.POST)
    #         if form.is_valid():
    #             profile = Seller.objects.create(
    #                 name=form.cleaned_data['name'],
    #                 country=form.cleaned_data['country'],
    #                 company=form.cleaned_data['company'],
    #                 phone=form.cleaned_data['phone'],
    #                 address=form.cleaned_data['address'],
    #                 #email=form.cleaned_data['email'],#Check for the essence of an email from the seller        
    #             )
    #             profile.save()
    #             #service.profile.add(profile)#Add the newly created profile to the service request
    #             return redirect('seller:profile')#Redirect to the seller profile page
    #     else:
    #         form = ProfileForm() 
    #     context = {
    #         'form': form,
    #         'profile': profile,#You may not want to display a contact message/returns the newly created profile object
    #     }           
    #     return render(request, 'seller/register.html', context)


    # def sort_products():
    #         for item in 
    #     #Filter the keys of the dictionary to find out which products were actually sold today or in a given period of time
    #     for item in sold_products.keys():
    #         n_time = datetime.datetime.now()
    #         today = n_time.date()
    #         if item.date_ordered == today:
    #             print(item)
    #         else:
    #             return "None was sold today"   