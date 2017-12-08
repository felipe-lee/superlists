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

    return redirect(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))


def view_list(request, list_id):
    """
    View to see a single list
    """
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'list': list_})


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)

    return redirect(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))
