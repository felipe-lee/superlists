# -*- coding: utf-8 -*-
"""
Handle authentication for project
"""
from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    """
    Handles authentication based on email-only.
    """
    
    @staticmethod
    def authenticate(uid):
        """
        Retrieve or create user if token is valid
        :param uid: token uid
        :return: user or None
        """
        try:
            token = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return None
        
        try:
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
    
    @staticmethod
    def get_user(email):
        """
        Retrieve a user by email
        :param email: user email
        :return: user or None
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
