# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from lists.models import Item, List


def home_page(request):
    """
    Home page view
    """
    return render(request, 'lists/home.html')


def new_list(request):
    """
    View to create a new list and add the first item to the list.
    """
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        
        return render(request, 'lists/home.html', {'error': error})
    else:
        item.save()

    return redirect(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))


def view_list(request, list_id):
    """
    View to see a single list
    :param list_id: ID of list to view.
    """
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))
    
    return render(request, 'lists/list.html', {'list': list_})
