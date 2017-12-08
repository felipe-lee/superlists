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


class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        """
        Setup browser for tests
        """
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()
    
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

    def test_can_start_a_list_and_retrieve_it_later(self):
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
        inputbox.send_keys('Buy cat toys')
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy cat toys" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy cat toys')
        
        # There is still a text box inviting her to add another item. She enters "Surprise cats with toys"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Surprise cats with toys')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy cat toys')
        self.wait_for_row_in_list_table('2: Surprise cats with toys')

        # The page updates again, and now shows both items on her list

        # Emily wonders whether the site will remember her list. Then she sees that teh site has generated a unique url
        # for her -- there is some explanatory text to that effect.
        self.fail('Finish the test!')
        
        # She visits that URL - her to-do list is still there.
        
        # Satisfied, she goes to sleep.
