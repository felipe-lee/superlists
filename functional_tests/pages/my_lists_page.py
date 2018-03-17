# -*- coding: utf-8 -*-
"""
My lists page object
"""


class MyListsPage(object):
    """
    Object to keep track of my lists page
    """

    def __init__(self, test):
        """
        page test
        :param test: test that is using this object
        """
        self.test = test

    def go_to_my_lists_page(self):
        """
        Navigates to user's lists page
        :return: self
        """
        self.test.browser.get(self.test.live_server_url)

        self.test.browser.find_element_by_link_text('My lists').click()

        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My Lists'
        ))

        return self
