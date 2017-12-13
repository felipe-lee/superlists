# -*- coding: utf-8 -*-
"""
Tests for lists forms
"""
from django.test import TestCase

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
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

    def test_form_save_handles_saving_to_a_list(self):
        text = 'do me'
        list_ = List.objects.create()
        form = ItemForm(data={'text': text})
        new_item = form.save(for_list=list_)
    
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, list_)


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
