# -*- coding: utf-8 -*-
"""
List item validation FTs
"""
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

E_ITEM_1 = 'Buy salmon'
E_ITEM_2 = 'Make salmon dinner'


class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Emily goes to the home page and accidentally tries to submit an empty list item. She hits enter on the empty
        # input box.
        self.browser.get(self.live_server_url)
        self.enter_input('')

        # The browser intercepts the request, and does not load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # She starts typing some text for the new item and the error disappears
        self.set_inputbox()
        self.inputbox.send_keys(E_ITEM_1)

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        # And she can submit it successfully
        self.inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        
        # Perversely, she now decides to submit a second blank list item
        self.enter_input('')

        # Again the browser will not comply
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # And she can correct it filling some text in
        self.set_inputbox()
        self.inputbox.send_keys(E_ITEM_2)

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        self.inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        self.wait_for_row_in_list_table(f'2: {E_ITEM_2}')

    def test_cannot_add_duplicate_items(self):
        # Emily goes to the new home page and starts a new list
        self.browser.get(self.live_server_url)
    
        self.enter_input(E_ITEM_1)
    
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
    
        # She accidentally tries to enter a duplicate item
        self.enter_input(E_ITEM_1)
    
        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            "You've already got this in your list"
        ))
