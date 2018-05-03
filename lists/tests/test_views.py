# -*- coding: utf-8 -*-
"""
Base tests for lists app
"""
import unittest
from unittest.mock import Mock, patch

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.html import escape

from accounts.models import User
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
from lists.models import Item, List
from lists.views import new_list


class HomePageTest(TestCase):
    
    def test_uses_home_template(self):
        response = self.client.get(reverse_lazy('home'))
    
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse_lazy('home'))
    
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListViewIntegratedTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        list_text = 'A new list item'
    
        self.client.post(reverse_lazy('lists:new_list'), data={'text': list_text})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, list_text)

    def test_invalid_input_doesnt_save_but_shows_errors(self):
        response = self.client.post(reverse_lazy('lists:new_list'), data={'text': ''})
    
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
    
        self.client.force_login(user)

        self.client.post(reverse_lazy('lists:new_list'), data={'text': 'new item'})

        list_ = List.objects.first()

        self.assertEqual(user, list_.owner)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    
    def setUp(self):
        """
        Sets up a request and post dict
        """
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()
    
    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        # Allows redirect to resolve correctly when it gets the absolute url of the model instance
        mockNewListForm.return_value.save.return_value.get_absolute_url.return_value = '/lists/1/'

        new_list(self.request)
        
        mockNewListForm.assert_called_once_with(data=self.request.POST)
    
    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        
        # Allows redirect to resolve correctly when it gets the absolute url of the model instance
        mock_form.save.return_value.get_absolute_url.return_value = '/lists/1/'

        new_list(self.request)
        
        mock_form.save.assert_called_once_with(owner=self.request.user)
    
    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)
        
        self.assertEqual(response, mock_redirect.return_value)
        
        mock_redirect.assert_called_once_with(mock_form.save.return_value)
    
    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)
        
        self.assertEqual(response, mock_render.return_value)
        
        mock_render.assert_called_once_with(self.request, 'lists/home.html', {'form': mock_form})
    
    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        new_list(self.request)
        
        self.assertFalse(mock_form.save.called)


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

        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
    
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
    
        response = self.client.get(reverse_lazy('lists:view_list', kwargs={'list_id': list_.id}))

        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        text = 'textey'
        list_1 = List.objects.create()
        item_1 = Item.objects.create(list=list_1, text=text)
    
        response = self.client.post(reverse_lazy('lists:view_list', kwargs={'list_id': list_1.id}),
                                    data={'text': text})
    
        expected_error = escape(DUPLICATE_ITEM_ERROR)
    
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
    
        self.assertEqual(new_item, Item.objects.first())


class MyListsTest(TestCase):
    
    def test_my_lists_url_renders_my_list_template(self):
        user_email = 'a@b.com'
    
        User.objects.create(email=user_email)
    
        response = self.client.get(reverse_lazy('lists:my_lists', kwargs={'user_email': user_email}))
        
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
    
        correct_user_email = 'a@b.com'
    
        correct_user = User.objects.create(email=correct_user_email)
    
        response = self.client.get(reverse_lazy('lists:my_lists', kwargs={'user_email': correct_user_email}))
    
        self.assertEqual(correct_user, response.context['owner'])


class ShareListTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Set up data for tests
        """
        super().setUpClass()
        
        cls.user = User.objects.create(email='a@b.com')
        
        cls.list_to_share = List.create_new('random item', owner=cls.user)
        
        cls.post_data = {'sharee': 'other@b.com'}
    
    def test_post_redirects_to_lists_page(self):
        response = self.client.post(reverse_lazy('lists:share_list', kwargs={'list_id': self.list_to_share.id}),
                                    data=self.post_data)
        
        self.assertEqual(reverse_lazy('lists:view_list', kwargs={'list_id': self.list_to_share.id}), response.url)
    
    def test_saves_sharee_email_to_shared_with_field(self):
        self.client.post(reverse_lazy('lists:share_list', kwargs={'list_id': self.list_to_share.id}),
                         data=self.post_data)
        
        user_shared_with = User.objects.get(email=self.post_data['sharee'])
        
        self.assertIn(user_shared_with, self.list_to_share.shared_with.all())
    
    def test_if_sharee_isnt_a_user_then_add_them_as_a_user(self):
        try:
            user_to_share_with = User.objects.get(email=self.post_data['sharee'])
        except User.DoesNotExist:
            pass
        else:
            user_to_share_with.delete()
        
        self.client.post(reverse_lazy('lists:share_list', kwargs={'list_id': self.list_to_share.id}),
                         data=self.post_data)
        
        self.assertIn(self.post_data['sharee'], User.objects.values_list('email', flat=True))
