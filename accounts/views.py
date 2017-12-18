# -*- coding: utf-8 -*-
"""
Views for accounts app
"""
import sys
import uuid

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.models import Token


def send_login_email(request):
    """
    Send user email to login to website
    """
    email = request.POST['email']

    uid = str(uuid.uuid4())

    Token.objects.create(email=email, uid=uid)

    print(f'Saving uid ({uid}) for email: {email}.', file=sys.stderr)

    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')

    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email]
    )

    return render(request, 'accounts/login_email_sent.html')


def login(request):
    """
    Log a user in after they click on the link
    """
    print('login view', file=sys.stderr)

    uid = request.GET.get('uid')

    user = authenticate(uid=uid)

    if user is not None:
        auth_login(request, user)

    return redirect(reverse_lazy('home'))


def logout(request):
    """
    Log user out of site
    """
    auth_logout(request)

    return redirect(reverse_lazy('home'))
