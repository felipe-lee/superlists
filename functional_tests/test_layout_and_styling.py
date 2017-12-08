# -*- coding: utf-8 -*-
"""
Layout and styling functional tests
"""

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    
    def test_aesthetics(self):
        # Emily goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        
        # She starts a new list and sees the input is nicely centered there too
        new_text = 'random item'
        
        inputbox.send_keys(new_text)
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table(f'1: {new_text}')
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
