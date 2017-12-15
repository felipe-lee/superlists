# -*- coding: utf-8 -*-
"""
Views for accounts app
"""
import uuid

from accounts.models import Token


def send_login_email(request):
    """
    Send user email to login to website
    """
    email = request.POST['email']

    uid = str(uuid.uuid4())

    Token.objects.create(email=email, uid=uid)

    print(f'Saving uid ({uid}) for email: {email}. | {')
