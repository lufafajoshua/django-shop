from django.urls import include, path
from . import views
from user_profiles.views import CustomerSignUpView, UserAgentSignUpView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'user_profiles'
urlpatterns = [
    path('register-customer/', CustomerSignUpView.as_view(), name='register-customer'),
    path('register-agent/', UserAgentSignUpView.as_view(), name='register-agent'), 
    path('mylogin/', views.mylogin, name='login'),#Handle login for a particular user
    path('mylogout/', views.mylogout, name='user_logout'),
    path('accounts/login/', LoginView),
    path('login_success/', views.login_success, name='login_success'),
]

