# -*- coding: utf-8 -*-
"""
Functional tests for TDD
"""
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    
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
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Emily has heard about a cool new online to-do app. She goes to check out its homepage
        self.browser.get('http://localhost:8000')
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # She types "Buy cat toys" into a text box (She has multiple cats that love to play)
        inputbox.send_keys('Buy cat toys')
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy cat toys" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy cat toys' for row in rows),
            "New to-do item did not appear in table"
        )
        # There is still a text box inviting her to add another item. She enters "Surprise cats with toys"
        self.fail('Finish the test!')
        # The page updates again, and now shows both items on her list
        
        # Edith wonders whether the site will remember her list. Then she sees that teh site has generated a unique url
        # for her -- there is some explanatory text to that effect.
        
        # She visits that URL - her to-do list is still there.
        
        # Satisfied, she goes to sleep.


if __name__ == '__main__':
    unittest.main()
