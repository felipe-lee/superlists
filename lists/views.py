# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.core.exceptions import ValidationError
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

    return redirect(list_)


def view_list(request, list_id):
    """
    View to see a single list
    :param list_id: ID of list to view.
    """
    list_ = List.objects.get(id=list_id)
    context = {'list': list_}

    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
    
        try:
            item.full_clean()
        except ValidationError:
            context['error'] = "You can't have an empty list item"
        else:
            item.save()

            return redirect(list_)

    return render(request, 'lists/list.html', context)
