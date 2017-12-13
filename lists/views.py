# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    """
    Home page view
    """
    return render(request, 'lists/home.html', {'form': ItemForm()})


def new_list(request):
    """
    View to create a new list and add the first item to the list.
    """
    form = ItemForm(data=request.POST)

    if form.is_valid():
        list_ = List.objects.create()
    
        Item.objects.create(text=request.POST['text'], list=list_)
    
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})


def view_list(request, list_id):
    """
    View to see a single list
    :param list_id: ID of list to view.
    """
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    
    context = {'list': list_}

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
    
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            
            return redirect(list_)

    context['form'] = form
    
    return render(request, 'lists/list.html', context)
