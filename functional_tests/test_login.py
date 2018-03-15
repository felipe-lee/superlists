# -*- coding: utf-8 -*-
"""
Test user login
"""
import re

from functional_tests.list_page import ListPage
from .base import FunctionalTest

TEST_EMAIL = 'santiago.garcia.flg@gmail.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Emily goes to the awesome superlists site and notices a "Log in" section in the navbar for the first time.
        # It's telling her to enter her email address, so she does.
        self.browser.get(self.live_server_url)

        list_page = ListPage(self)
        list_page.enter_email(TEST_EMAIL)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(TEST_EMAIL, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)

        url_search = re.search(r'http://.+/.+$', body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')

        url = url_search.group(0)

        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        list_page.wait_to_be_logged_in(email=TEST_EMAIL)
        
        # Now she logs out
        list_page.click_log_out_link()

        # She is logged out
        list_page.wait_to_be_logged_out(email=TEST_EMAIL)
