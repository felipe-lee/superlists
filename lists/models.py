# -*- coding: utf-8 -*-
"""
Lists models
"""
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class List(models.Model):
    """
    Model to keep track of lists
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        """
        Retrieve url to view list in live website
        :return: list url in live website
        """
        return reverse_lazy('lists:view_list', kwargs={'list_id': self.id})

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    """
    Model to keep track of our list items
    """
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
