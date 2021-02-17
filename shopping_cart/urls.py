from django.urls  import path

from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-summary/', views.order_details, name='order_summary'),
    path('success/', views.success, name='purchase_success'),
    path('item/delete/<int:item_id>/', views.delete_from_cart, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-transaction/<int:order_id>', views.update_transaction_records, name='update_records'),
    path('sold_order/<int:order_id>', views.sold_details, name='sold_order'),
    path('sold_orders/', views.sold_orders, name='sold_orders'),
    path('process-payment/', views.make_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('my_orders/', views.my_orders, name='my_orders')
    
]