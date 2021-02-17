from django.urls  import path

from . import views
from seller.views import SellerSignUpView

app_name = 'seller'
urlpatterns = [
    path('sellers/', views.all_sellers, name='sellers'),
    path('detail/<int:seller_id>', views.seller_detail, name='seller_detail'),
    path('register-seller/', SellerSignUpView.as_view(), name='register-seller'),
    #path('create_profile/', views.create_profile, name='profile'),
    path('login/', views.sellerlogin, name='login'),
    path('seller_profile/', views.seller_profile, name='profile'),
   
]
