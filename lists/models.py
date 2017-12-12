# -*- coding: utf-8 -*-
"""
Lists models
"""
from django.db import models
from django.urls import reverse_lazy


class List(models.Model):
    """
    Model to keep track of lists
    """
    
    def get_absolute_url(self):
        """
        Retrieve url to view list in live website
        :return: list url in live website
        """
        return reverse_lazy('lists:view_list', kwargs={'list_id': self.id})


class Item(models.Model):
    """
    Model to keep track of our list items
    """
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    text = models.TextField(default='')
