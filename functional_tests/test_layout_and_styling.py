# -*- coding: utf-8 -*-
"""
Layout and styling functional tests
"""

from functional_tests.base import FunctionalTest
from functional_tests.pages.list_page import ListPage


class LayoutAndStylingTest(FunctionalTest):
    
    def test_aesthetics(self):
        # Emily goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        list_page = ListPage(self)

        # She notices the input box is nicely centered
        input_box = list_page.get_item_input_box()

        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
        
        # She starts a new list and sees the input is nicely centered there too
        new_text = 'random item'

        list_page.add_list_item(new_text)

        input_box = list_page.get_item_input_box()
        
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
