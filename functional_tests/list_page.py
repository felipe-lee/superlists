# -*- coding: utf-8 -*-
"""
List page objects to help keep FTs cleaner
"""
from selenium.webdriver.common.keys import Keys

from .base import wait


class ListPage(object):
    """
    Object to keep track of all the information about the list page to make it easier to maintain.
    """

    def __init__(self, test):
        """
        Sets up test object
        :param test: test being run
        """
        self.test = test

    def get_table_rows(self):
        """
        Finds table rows in dom.
        :return: table rows
        """
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        """
        Wait for row to appear in the list.
        :param item_text: Text to add as list item
        :param item_number: Item's place on the list.
        """
        expected_row_text = f'{item_number}: {item_text}'

        rows = self.get_table_rows()

        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_item_input_box(self):
        """
        Retrieves the input box from the dom
        :return: input box element
        """
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        """
        Adds an item to the list and tests that it is added correctly.
        :param item_text: Text to add as a list item.
        :return: self
        """
        new_item_no = len(self.get_table_rows()) + 1

        input_box = self.get_item_input_box()
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(item_text, new_item_no)

        return self

    def get_share_box(self):
        """
        Retrieves the share box from the dom
        :return: share box input element
        """
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

    def get_shared_with_list(self):
        """
        Retrieves list of people that the to-do list is shared with
        :return: list of sharees
        """
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )

    def share_list_with(self, email):
        """
        Shares to-do list with the input email and tests to ensure it was shared correctly.
        :param email: email to share the list with
        """
        share_box = self.get_share_box()
        share_box.send_keys(email)
        share_box.send_keys(Keys.ENTER)

        self.test.wait_for(lambda: self.test.assertIn(
            email, [person.text for person in self.get_shared_with_list()]
        ))
