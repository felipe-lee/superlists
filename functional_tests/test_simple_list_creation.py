# -*- coding: utf-8 -*-
"""
Functional tests for TDD
"""
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_TIME = 10
E_ITEM_1 = 'Buy cat toys'
E_ITEM_2 = 'Surprise cats with toys'
F_ITEM_1 = 'Look for deals on computer parts'
F_ITEM_2 = 'Build a new computer'


def get_webdriver():
    """
    Setup a webdriver
    """
    return webdriver.Chrome()
    # return webdriver.Firefox()


class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        """
        Setup browser for tests
        """
        self.browser = get_webdriver()
    
    def tearDown(self):
        """
        Clean up after tests.
        """
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Waits for table to appear on page and checks if row_text is in any row.
        :param row_text: Text to search for in row
        """
        start_time = time.time()
    
        def check_time(exc):
            """
            Checks if we should wait longer or not
            :return:
            """
            if time.time() - start_time > MAX_TIME:
                raise exc
        
            time.sleep(0.5)
    
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
            except WebDriverException as e:
                check_time(e)
            
                continue
            else:
                rows = table.find_elements_by_tag_name('tr')
        
            try:
                self.assertIn(row_text, [row.text for row in rows])
            except AssertionError as e:
                check_time(e)
            
                continue
            else:
                break

    def test_can_start_a_list_for_one_user(self):
        # Emily has heard about a cool new online to-do app. She goes to check out its homepage
        self.browser.get(self.live_server_url)
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        # She types "Buy cat toys" into a text box (She has multiple cats that love to play)
        inputbox.send_keys(E_ITEM_1)
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy cat toys" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        
        # There is still a text box inviting her to add another item. She enters "Surprise cats with toys"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(E_ITEM_2)
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        self.wait_for_row_in_list_table(f'2: {E_ITEM_2}')

        # Satisfied, she goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Emily starts a new to-do list
        self.browser.get(self.live_server_url)
    
        inputbox = self.browser.find_element_by_id('id_new_item')
    
        inputbox.send_keys(E_ITEM_1)
        inputbox.send_keys(Keys.ENTER)
    
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
    
        # She notices that her list has a unique URL.
        emily_list_url = self.browser.current_url
        self.assertRegex(emily_list_url, '/lists/.+')
    
        # Now a new user, Felipe, comes along to teh site.
    
        # # We use a new browser session to make sure that no information of Emily's is coming through from cookies,
        self.browser.quit()
    
        self.browser = get_webdriver()
    
        # Felipe visits the home page. There is no sign of Emily's list
        self.browser.get(self.live_server_url)
    
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn(E_ITEM_1, page_text)
        self.assertNotIn(E_ITEM_2, page_text)
    
        # Felipe starts a new list by entering a new item. He is into techy stuff...
        inputbox = self.browser.find_element_by_id('id_new_item')
    
        inputbox.send_keys(F_ITEM_1)
        inputbox.send_keys(Keys.ENTER)
    
        self.wait_for_row_in_list_table(f'1: {F_ITEM_1}')
    
        # Felipe gets his own unique URL
        felipe_list_url = self.browser.current_url
        self.assertRegex(felipe_list_url, '/lists/.+')
        self.assertNotEqual(felipe_list_url, emily_list_url)
    
        # Again, there is no trace of Emily's list
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn(E_ITEM_1, page_text)
        self.assertNotIn(E_ITEM_2, page_text)
    
        # Satisfied, they both go back to sleep
