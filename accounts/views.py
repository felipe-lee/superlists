# -*- coding: utf-8 -*-
"""
Accounts app views
"""
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy

from accounts.models import Token


def send_login_email(request):
    """
    View to handle sending login emails upon request.
    """
    email = request.POST['email']
    
    token = Token.objects.create(email=email)
    
    url = request.build_absolute_uri(
        f"{reverse_lazy('accounts:login')}?token={str(token.uid)}"
    )
    
    message_body = f'Use this link to log in:\n\n{url}'
    
    send_mail(
        subject='Your login link for Superlists',
        message=message_body,
        from_email='noreply@superlists',
        recipient_list=[email]
    )
    
    messages.success(request, "Check your email, we've sent you a link you can use to log in.")
    
    return redirect(reverse_lazy('home'))


def login(request):
    """
    View to login users
    """
    user = auth.authenticate(uid=request.GET.get('token'))

    if user:
        auth.login(request, user)

    return redirect(reverse_lazy('home'))
