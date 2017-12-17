# -*- coding: utf-8 -*-
"""
Superlists authentication
"""
import sys

from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(object):
    """
    Authentication manager for superlists
    """

    def authenticate(self, uid):
        """
        Authenticate the uid input and return an email
        """
        print(f'uid {uid}', file=sys.stderr)

        if not Token.objects.filter(uid=uid).exists():
            print('No token found', file=sys.stderr)

            return None

        token = Token.objects.get(uid=uid)

        print('Get token', file=sys.stderr)

        try:
            user = ListUser.objects.get(email=token.email)
        except ListUser.DoesNotExist:
            print('New user', file=sys.stderr)

            return ListUser.objects.create(email=token.email)
        else:
            print('Got user', file=sys.stderr)

            return user

    def get_user(self, email):
        """
        Gets a user based on email
        """
        return ListUser.objects.get(email=email)
