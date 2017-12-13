# -*- coding: utf-8 -*-
"""
Forms for lists app
"""
from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):
    """
    Form to handle adding items to lists
    """
    
    class Meta:
        """
        Define what model info to use.
        """
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
