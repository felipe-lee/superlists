# -*- coding: utf-8 -*-
"""
Simple list creation FTs
"""

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from functional_tests.helpers import get_webdriver
from functional_tests.list_page import ListPage

E_ITEM_1 = 'Buy cat toys'
E_ITEM_2 = 'Surprise cats with toys'
F_ITEM_1 = 'Look for deals on computer parts'
F_ITEM_2 = 'Build a new computer'


class NewVisitorTest(FunctionalTest):
    
    def test_can_start_a_list_for_one_user(self):
        # Emily has heard about a cool new online to-do app. She goes to check out its homepage
        self.browser.get(self.live_server_url)
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # She is invited to enter a to-do item straight away
        list_page = ListPage(self)
        input_box = list_page.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
        
        # She types "Buy cat toys" into a text box (She has multiple cats that love to play)
        input_box.send_keys(E_ITEM_1)
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy cat toys" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        
        # There is still a text box inviting her to add another item. She enters "Surprise cats with toys"
        list_page.enter_list_item(E_ITEM_2)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        self.wait_for_row_in_list_table(f'2: {E_ITEM_2}')

        # Satisfied, she goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Emily starts a new to-do list
        self.browser.get(self.live_server_url)

        list_page = ListPage(self).add_list_item(E_ITEM_1)
    
        # She notices that her list has a unique URL.
        emily_list_url = self.browser.current_url
        self.assertRegex(emily_list_url, '/lists/.+')

        # Now a new user, Felipe, comes along to the site.
    
        # # We use a new browser session to make sure that no information of Emily's is coming through from cookies,
        self.browser.refresh()
        self.browser.quit()
    
        self.browser = get_webdriver()
    
        # Felipe visits the home page. There is no sign of Emily's list
        self.browser.get(self.live_server_url)
    
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn(E_ITEM_1, page_text)
        self.assertNotIn(E_ITEM_2, page_text)
    
        # Felipe starts a new list by entering a new item. He is into techy stuff...
        list_page.add_list_item(F_ITEM_1)
    
        # Felipe gets his own unique URL
        felipe_list_url = self.browser.current_url
        self.assertRegex(felipe_list_url, '/lists/.+')
        self.assertNotEqual(felipe_list_url, emily_list_url)
    
        # Again, there is no trace of Emily's list
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn(E_ITEM_1, page_text)
        self.assertNotIn(E_ITEM_2, page_text)
    
        # Satisfied, they both go back to sleep
