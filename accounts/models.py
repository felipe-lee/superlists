# -*- coding: utf-8 -*-
"""
Models for accounts app
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Token(models.Model):
    """
    Keep track of user login tokens.
    """
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):

    @staticmethod
    def create_user(email):
        """
        Shortcut to create a user with only an email.
        """
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """
        Create a superuser without a password.
        """
        self.create_user(email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    """
    Keep track of all users.
    """
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'height']

    objects = ListUserManager()

    @property
    def is_staff(self):
        """
        Check if email matches a staff email
        """
        return self.email == 'santiago.garcia.flg@gmail.com'

    @property
    def is_active(self):
        """
        ?
        """
        return True
