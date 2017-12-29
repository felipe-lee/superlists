# -*- coding: utf-8 -*-
"""
Base Functional Test
"""
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from functional_tests.helpers import get_webdriver

MAX_TIME = 10


def wait(fn):
    """
    Wraps input function in a function that waits for input function to be callable without an Exception
    :param fn: function to attempt to call
    :return: wrapped function
    """
    
    def modified_fn(*args, **kwargs):
        """
        Handles wait functionality
        """
        start_time = time.time()
        
        while True:
            try:
                return fn(*args, **kwargs)
            except (WebDriverException, AssertionError) as exc:
                if time.time() - start_time > MAX_TIME:
                    raise exc
                
                time.sleep(0.5)
    
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        """
        Setup browser for tests
        """
        self.browser = get_webdriver()

        staging_server = os.environ.get('STAGING_SERVER')

        if staging_server:
            self.live_server_url = f'http://{staging_server}'
    
    def tearDown(self):
        """
        Clean up after tests.
        """
        self.browser.refresh()
        self.browser.quit()

    def set_inputbox(self):
        """
        Gets inputbox. Seems almost pointless but useful to stop repeating name of input box.
        """
        self.inputbox = self.browser.find_element_by_id('id_text')

    def enter_input(self, text_to_input):
        """
        Shortcut to enter input in inputbox
        :param text_to_input: Text to input in self.inputbox
        """
        self.set_inputbox()
        
        self.inputbox.send_keys(text_to_input)
        self.inputbox.send_keys(Keys.ENTER)

    @staticmethod
    @wait
    def wait_for(fn):
        """
        Waits for function to be callable without an Exception
        :param fn: function to attempt to call
        :return: wrapped function
        """
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        """
        Waits for table to appear on page and checks if row_text is in any row.
        :param row_text: Text to search for in row
        """

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        """
        Waits for user to be logged in.
        :param email: user email
        """
        self.browser.find_element_by_link_text('Log out')
    
        navbar = self.browser.find_element_by_css_selector('.navbar')
    
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """
        Wait for user to be logged out.
        :param email: user email
        """
        self.browser.find_element_by_name('email')
    
        navbar = self.browser.find_element_by_css_selector('.navbar')
    
        self.assertNotIn(email, navbar.text)
