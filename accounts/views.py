# -*- coding: utf-8 -*-
"""
Views for accounts app
"""
import sys
import uuid

from django.core.mail import send_mail
from django.shortcuts import render

from accounts.models import Token


def send_login_email(request):
    """
    Send user email to login to website
    """
    email = request.POST['email']

    uid = str(uuid.uuid4())

    Token.objects.create(email=email, uid=uid)

    print(f'Saving uid ({uid}) for email: {email}. | {file=sys.stderr}')

    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')

    send_mail(
        'Your loign link for Superslists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email]
    )

    return render(request, 'accounts/login_email_sent.html')
