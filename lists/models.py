# -*- coding: utf-8 -*-
"""
Lists models
"""
from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    """
    Model to keep track of our list items
    """
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    text = models.TextField(default='')
