# -*- coding: utf-8 -*-
"""
Base Functional Test
"""
import time

from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

from functional_tests.helpers import get_webdriver

MAX_TIME = 10


class FunctionalTest(LiveServerTestCase):
    
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
