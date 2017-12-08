# -*- coding: utf-8 -*-
"""
Base tests for lists app
"""
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
    
        self.assertTemplateUsed(response, 'lists/home.html')


class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        list_item_text = 'A new list item'

        self.client.post('/lists/new', data={'item_text': list_item_text})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, list_item_text)

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_list_items(self):
        text_1 = 'itemy 1'
        text_2 = 'itemy 2'

        Item.objects.create(text=text_1)
        Item.objects.create(text=text_2)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, text_1)
        self.assertContains(response, text_2)
