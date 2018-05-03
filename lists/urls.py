# -*- coding: utf-8 -*-
"""
Lists app URL Configuration
"""
from django.urls import path

from lists.views import my_lists, new_list, share_list, view_list

app_name = 'lists'
urlpatterns = [
    path('new', new_list, name='new_list'),
    path('<int:list_id>/', view_list, name='view_list'),
    path('users/<user_email>', my_lists, name='my_lists'),
    path('share-list/<int:list_id>', share_list, name='share_list'),
]
