# -*- coding: utf-8 -*-
"""
List item validation FTs
"""
from functional_tests.base import FunctionalTest

E_ITEM_1 = 'Buy salmon'
E_ITEM_2 = 'Make salmon dinner'


class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Emily goes to the home page and accidentally tries to submit an empty list item. She hits enter on the empty
        # input box.
        self.browser.get(self.live_server_url)
        self.enter_input('')
        
        # The home page refreshes, and there is an error message saying that list items cannot be blank.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You can\'t have an empty list item'
        ))
        
        # She tries again with some text for the item, which now works
        self.enter_input(E_ITEM_1)
        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        
        # Perversely, she now decides to submit a second blank list item
        self.enter_input('')
        
        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You can\'t have an empty list item'

        ))

        # And she can correct it filling some text in
        self.enter_input(E_ITEM_2)

        self.wait_for_row_in_list_table(f'1: {E_ITEM_1}')
        self.wait_for_row_in_list_table(f'2: {E_ITEM_2}')
