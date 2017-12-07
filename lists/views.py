# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import render


def home_page(request):
    return render(request, 'lists/home.html')
