# -*- coding: utf-8 -*-
"""
Forms for lists app
"""
from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


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

    def save(self, for_list, commit=True):
        """
        Override save method to pass in list
        :param for_list: list to save item to
        :param commit: commit save boolean.
        """
        self.instance.list = for_list
    
        return super().save(commit)


class ExistingListItemForm(ItemForm):
    """
    Form to handle adding items to list without adding duplicates
    """
    
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.instance.list = for_list
    
    def validate_unique(self):
        """
        Override default validation message
        """
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            
            self._update_errors(e)
