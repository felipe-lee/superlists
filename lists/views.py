# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import redirect, render

from accounts.models import User
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List


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
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()

        form.save(for_list=list_)
    
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})


def new_list2(request):
    """
    View to create a new list and add the first item to the list.
    """
    form = NewListForm(data=request.POST)
    
    if form.is_valid():
        list_ = form.save(owner=request.user)
        
        return redirect(list_)
    
    return render(request, 'lists/home.html', {'form': form})


def view_list(request, list_id):
    """
    View to see a single list
    :param request: request
    :param list_id: ID of list to view.
    """
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    
    context = {'list': list_}

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
    
        if form.is_valid():
            form.save()
            
            return redirect(list_)

    context['form'] = form
    
    return render(request, 'lists/list.html', context)


def my_lists(request, user_email):
    """
    View to see a user's lists
    :param request: request
    :param user_email: email of user whose lists should be shown.
    """
    owner = User.objects.get(email=user_email)
    
    return render(request, 'lists/my_lists.html', {'owner': owner})
