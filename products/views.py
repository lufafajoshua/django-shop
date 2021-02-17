from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from shopping_cart.models import Order
from .models import Product, Category
from django.db.models import Q
from .forms import SearchForm

@login_required
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    #Unpack the order object to retrieve the order items selected by the user 
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "products/product_list.html", context)

@login_required
def category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }  
    return render(request, 'products/category.html', context)

@login_required
def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = category.product_set.all()#Display these from the template
    context = {
        'category': category,
        'product': products,
    }
    return render(request, 'products/category_detail.html')

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    form = SearchForm()
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(name__icontains=query) | Q(description__icontains=query)
            results= Product.objects.filter(lookups).distinct()
            context = {
                'results': results,
                'submitbutton': submitbutton,
            }
            return render(request, 'products/search.html', context)
        else:
            return render(request, 'products/search.html')  
    else:
        return render(request, 'products/search.html')



