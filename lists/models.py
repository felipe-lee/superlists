# -*- coding: utf-8 -*-
"""
Lists models
"""
from django.db import models


class Item(models.Model):
    """
    Model to keep track of our list items
    """
    text = models.TextField(default='')
