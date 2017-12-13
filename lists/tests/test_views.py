# -*- coding: utf-8 -*-
"""
Base tests for lists app
"""
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class HomePageTest(TestCase):
    
    def test_uses_home_template(self):
        response = self.client.get(reverse_lazy('home'))
    
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse_lazy('home'))
    
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        list_text = 'A new list item'
    
        self.client.post(reverse_lazy('lists:new_list'), data={'text': list_text})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, list_text)

    def test_redirects_after_POST(self):
        response = self.client.post(reverse_lazy('lists:new_list'), data={'text': 'A new list item'})

        new_list = List.objects.first()
    
        self.assertRedirects(response, reverse_lazy('lists:view_list', kwargs={'list_id': new_list.id}))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse_lazy('lists:new_list'), data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse_lazy('lists:new_list'), data={'text': ''})
    
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse_lazy('lists:new_list'), data={'text': ''})
    
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(reverse_lazy('lists:new_list'), data={'text': ''})
    
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))

        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        text_1 = 'itemy 1'
        text_2 = 'itemy 2'
    
        Item.objects.create(text=text_1, list=correct_list)
        Item.objects.create(text=text_2, list=correct_list)
    
        other_list = List.objects.create()
        o_text_1 = 'other list item 1'
        o_text_2 = 'other list item 2'
    
        Item.objects.create(text=o_text_1, list=other_list)
        Item.objects.create(text=o_text_2, list=other_list)

        response = self.client.get(reverse_lazy('lists:view_list', kwargs={'list_id': correct_list.id}))
        
        self.assertContains(response, text_1)
        self.assertContains(response, text_2)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(reverse_lazy('lists:view_list', kwargs={'list_id': correct_list.id}))
    
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text = 'A new item for an existing list'

        self.client.post(reverse_lazy('lists:view_list', kwargs={'list_id': correct_list.id}),
                         data={'text': text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text = 'A new item for an existing list'

        response = self.client.post(reverse_lazy('lists:view_list', kwargs={'list_id': correct_list.id}),
                                    data={'text': text})

        self.assertRedirects(response, reverse_lazy('lists:view_list', kwargs={'list_id': correct_list.id}))

    def post_invalid_input(self):
        """
        Posts invalid input to form
        :return: response to invalid input
        """
        list_ = List.objects.create()
    
        return self.client.post(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}), data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
    
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
    
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
    
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
    
        response = self.client.get(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))
    
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')
