# -*- coding: utf-8 -*-
"""
Tests for lists models
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import User
from lists.models import Item, List


class ListModelTest(TestCase):
    
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_lists_can_have_owners(self):
        user = User.objects.create(email='a@b.com')
    
        list_ = List.objects.create(owner=user)
    
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        self.assertTrue(List.objects.create())  # should not raise exception

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
    
        item_text_1 = 'first item'
        Item.objects.create(list=list_, text=item_text_1)
        Item.objects.create(list=list_, text='second item')
    
        self.assertEqual(item_text_1, list_.name)


class ItemModelsTest(TestCase):
    
    def test_default_text(self):
        item = Item()
        
        self.assertEqual(item.text, '')
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
    
        with self.assertRaises(ValidationError):
            item.save()

            item.full_clean()
    
    def test_duplicate_items_are_invalid(self):
        text = 'bla'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=text)
        
        with self.assertRaises(ValidationError):
            item = Item(list_, text=text)
            
            item.full_clean()
    
    def test_CAN_save_same_item_to_different_lists(self):
        text = 'bla'
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        
        Item.objects.create(list=list_1, text=text)
        item = Item(list=list_2, text=text)
        
        self.assertIsNone(item.full_clean())  # should not raise exception
    
    def test_list_ordering(self):
        list_1 = List.objects.create()
        
        item_1 = Item.objects.create(list=list_1, text='i1')
        item_2 = Item.objects.create(list=list_1, text='item 2')
        item_3 = Item.objects.create(list=list_1, text='3')

        self.assertEqual(list(Item.objects.all()), [item_1, item_2, item_3])
    
    def test_string_representation(self):
        text = 'some text'
        item = Item(text=text)
        
        self.assertEqual(str(item), text)
