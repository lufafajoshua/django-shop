from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/', views.category, name='category'),
    path('product-detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('category-detail/<int:category_id>', views.category_detail, name='category_detail'), 
    path('search', views.search, name='search'),    
]
