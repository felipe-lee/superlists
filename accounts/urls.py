# -*- coding: utf-8 -*-
"""
Urls for accounts app
"""
from django.urls import path

from accounts.views import send_login_email

app_name = 'accounts'
urlpatterns = [
    path('send_email', send_login_email, name='send_login_email')
]
