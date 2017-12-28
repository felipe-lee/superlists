# -*- coding: utf-8 -*-
"""
Accounts app URL Configuration
"""
from django.contrib.auth.views import logout
from django.urls import path, reverse_lazy

from accounts.views import login, send_login_email

app_name = 'accounts'
urlpatterns = [
    path('send-login-email', send_login_email, name='send_login_email'),
    path('login', login, name='login'),
    path('logout', logout, {'next_page': reverse_lazy('home')}, name='logout')
]
