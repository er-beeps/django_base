
from django.shortcuts import redirect
from django.urls import path, re_path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, logout_then_login
app_name = 'auth'

urlpatterns = [
    path('', redirect_login_view, name="login"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('auth/', redirect_login_view, name="redirect_login"),
    path('logout/', logout_then_login, name="logout"),
    path('password_change/', password_change, name="password_change"),
    
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('forgot_password/reset/<token>/', forgot_password_confirm, name="password_reset_confirm"),
]
