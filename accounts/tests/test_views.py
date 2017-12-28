# -*- coding: utf-8 -*-
"""
Tests for accounts app views
"""
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse_lazy

from accounts.models import Token

TEST_EMAIL = 'emily@knightsofhaven.net'


class SendLoginEmailViewTests(TestCase):
    
    def test_redirects_to_home_page(self):
        response = self.client.post(reverse_lazy('accounts:send_login_email'), data={'email': TEST_EMAIL})
        
        self.assertRedirects(response, reverse_lazy('home'))
    
    @patch('accounts.views.send_mail')
    def test_sends_email_to_address_from_post(self, mock_send_mail):
        self.client.post(reverse_lazy('accounts:send_login_email'), data={'email': TEST_EMAIL})
        
        self.assertTrue(mock_send_mail.called)
        
        args, kwargs = mock_send_mail.call_args
        
        self.assertEqual(kwargs.get('subject'), 'Your login link for Superlists')
        self.assertEqual(kwargs.get('from_email'), 'noreply@superlists')
        self.assertEqual(kwargs.get('recipient_list'), [TEST_EMAIL])
    
    def test_adds_success_message(self):
        response = self.client.post(reverse_lazy('accounts:send_login_email'), data={'email': TEST_EMAIL}, follow=True)
        
        message = list(response.context['messages'])[0]
        
        self.assertEqual(message.message, "Check your email, we've sent you a link you can use to log in.")
        
        self.assertEqual(message.tags, "success")
    
    def test_creates_token_associated_with_email(self):
        self.client.post(reverse_lazy('accounts:send_login_email'), data={'email': TEST_EMAIL})
        
        token = Token.objects.first()
        
        self.assertEqual(token.email, TEST_EMAIL)
    
    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_email):
        self.client.post(reverse_lazy('accounts:send_login_email'), data={'email': TEST_EMAIL})
        
        token = Token.objects.first()
        
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        
        args, kwargs = mock_send_email.call_args
        
        self.assertIn(expected_url, kwargs.get('message'))


TEST_TOKEN = 'abcd123'


class LoginViewTest(TestCase):
    
    def test_redirect_to_home_page(self):
        response = self.client.get(reverse_lazy('accounts:login'), data={'token': TEST_TOKEN})
        
        self.assertRedirects(response, reverse_lazy('home'))
