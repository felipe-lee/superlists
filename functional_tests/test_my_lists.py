# -*- coding: utf-8 -*-
"""
FTs for user lists
"""
from django.contrib.auth import get_user_model
from selenium.common.exceptions import NoSuchElementException

from functional_tests.list_page import ListPage
from .base import FunctionalTest

User = get_user_model()
TEST_EMAIL = 'emily@knightsofhaven.net'
E_ITEM_1 = 'Reticulate splines'
E_ITEM_2 = 'Immanentize eschaton'
E_ITEM_3 = 'Click cows'


class MyListsTest(FunctionalTest):
    
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Emily is a logged-in user
        self.create_pre_authenticated_session(TEST_EMAIL)

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)

        list_page = ListPage(self).add_list_item(E_ITEM_1).add_list_item(E_ITEM_2)

        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(E_ITEM_1)
        )

        self.browser.find_element_by_link_text(E_ITEM_1).click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)

        list_page.add_list_item(E_ITEM_3)

        second_list_url = self.browser.current_url

        # Under "My lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()

        self.wait_for(
            lambda: self.browser.find_element_by_link_text(E_ITEM_3)
        )

        self.browser.find_element_by_link_text(E_ITEM_3).click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My lists option disappears
        self.browser.find_element_by_link_text('Log out').click()

        self.wait_for(
            lambda: self.assertRaises(NoSuchElementException, self.browser.find_element_by_link_text, 'My lists')
        )
