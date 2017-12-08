# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from lists.models import Item, List


def home_page(request):
    """
    Home page view
    """
    return render(request, 'lists/home.html')


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)

    return redirect(reverse_lazy('view_list'))


def view_list(request):
    """
    View to see a single list
    """
    items = Item.objects.all()

    return render(request, 'lists/list.html', {'items': items})
