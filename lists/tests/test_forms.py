# -*- coding: utf-8 -*-
"""
Tests for lists forms
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List


class ItemFormTest(TestCase):
    
    def test_form_renders_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


class NewListFormTest(TestCase):
    
    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_post_data_if_user_not_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=False)
        
        new_item_text = 'new item text'
        form = NewListForm(data={'text': new_item_text})
        
        form.is_valid()
        
        form.save(owner=user)
        
        mock_List_create_new.assert_called_once_with(first_item_text=new_item_text)
    
    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_is_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        
        new_item_text = 'new item text'
        form = NewListForm(data={'text': new_item_text})
        
        form.is_valid()
        
        form.save(owner=user)
        
        mock_List_create_new.assert_called_once_with(first_item_text=new_item_text, owner=user)
    
    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        
        form = NewListForm(data={'text': 'new item text'})
        
        form.is_valid()
        
        response = form.save(owner=user)
        
        self.assertEqual(mock_List_create_new.return_value, response)


class ExistingListItemFormTest(TestCase):
    
    def test_form_renders_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
    
    def test_form_validation_for_duplicate_items(self):
        text = 'no twins!'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=text)
        form = ExistingListItemForm(for_list=list_, data={'text': text})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
