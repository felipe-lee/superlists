# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request):
    """
    Home page view
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    
    return render(request, 'lists/home.html')


def view_list(request):
    """
    View to see a single list
    """
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})
