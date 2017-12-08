# -*- coding: utf-8 -*-
"""
Layout and styling functional tests
"""

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    
    def test_aesthetics(self):
        # Emily goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # She notices the input box is nicely centered
        self.set_inputbox()
        self.assertAlmostEqual(
            self.inputbox.location['x'] + self.inputbox.size['width'] / 2,
            512,
            delta=10
        )
        
        # She starts a new list and sees the input is nicely centered there too
        new_text = 'random item'

        self.enter_input(new_text)
        
        self.wait_for_row_in_list_table(f'1: {new_text}')

        self.set_inputbox()
        
        self.assertAlmostEqual(
            self.inputbox.location['x'] + self.inputbox.size['width'] / 2,
            512,
            delta=10
        )
