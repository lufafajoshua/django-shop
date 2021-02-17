from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# Defined namespace for use on all templates
app_name = 'django_chatter'

urlpatterns = [
	path('', views.IndexView.as_view(), name = "index"),
	path('chat/<str:uuid>/', views.ChatRoomView.as_view(), name = "chatroom"),

	#AJAX paths
	path('ajax/users-list/', views.users_list, name = "users_list"),
	path('ajax/get-chat-url/', views.get_chat_url, name = "get_chat_url"),
	path('ajax/seller_chat/<int:product_id>', views.seller_chat, name = "seller_chat"),
	path('ajax/get-messages/<str:uuid>/', views.get_messages, name="get_messages"),
	path('register/', views.register, name='register'),
	path('accounts/login/', LoginView), 
]
