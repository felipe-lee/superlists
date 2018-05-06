# -*- coding: utf-8 -*-
"""
Lists views
"""
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView

from accounts.models import User
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List


class HomePageView(FormView):
    """
    Home page view
    """
    template_name = 'lists/home.html'
    form_class = ItemForm


class NewListView(CreateView):
    """
    View to see a single list
    """
    template_name = 'lists/home.html'
    form_class = NewListForm

    def form_valid(self, form):
        """
        Pass owner to form save.
        :param form: validated form
        :return: redirect
        """
        self.object = form.save(owner=self.request.user)
    
        return redirect(self.object)


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


def share_list(request, list_id):
    """
    View to share a list with an email.
    :param WSGIRequest request: request
    :param int list_id: id of list to share
    :return HttpResponseRedirect: redirect to lists view
    """
    list_ = List.objects.get(id=list_id)
    
    if request.POST.get('sharee'):
        try:
            user_to_share_with = User.objects.get(email=request.POST['sharee'])
        except User.DoesNotExist:
            user_to_share_with = User.objects.create(email=request.POST['sharee'])
        
        list_.shared_with.add(user_to_share_with)
    
    return redirect(list_)
