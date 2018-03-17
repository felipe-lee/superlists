# -*- coding: utf-8 -*-
"""
FTs to test sharing lists
"""
from functional_tests.pages.list_page import ListPage
from functional_tests.pages.my_lists_page import MyListsPage
from .base import FunctionalTest
from .helpers import get_webdriver

TEST_EMAIL_1 = 'emily@knightsofhaven.net'
TEST_EMAIL_2 = 'oniciferous@knightsofhaven.net'
TEST_ITEM = 'Hi Edith!'


def quit_if_possible(browser):
    """
    Try quitting browser
    :param browser: browser to quit
    """
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Emily is a logged in user
        self.create_pre_authenticated_session(TEST_EMAIL_1)

        emily_browser = self.browser

        self.addCleanup(lambda: quit_if_possible(emily_browser))

        # Her friend Oniciferous is also hanging out on the lists site
        oni_browser = get_webdriver()

        self.addCleanup(lambda: quit_if_possible(oni_browser))

        self.browser = oni_browser

        self.create_pre_authenticated_session(TEST_EMAIL_2)

        # Emily goes to the home page and starts a list
        self.browser = emily_browser

        self.browser.get(self.live_server_url)

        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()

        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@knightsofhaven.net')

        # She shares her list. The page updates to say that it's shared with Oniciferous
        list_page.share_list_with(TEST_EMAIL_2)

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser

        MyListsPage(self).go_to_my_lists_page()

        # He sees Edith's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oniciferous can see it says that it's Edit's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            TEST_EMAIL_1
        ))

        # He adds an item to the list
        list_page.add_list_item(TEST_ITEM)

        # When Edith refreshes the page, she sees Oniciferou's addition
        self.browser = emily_browser

        self.browser.refresh()

        list_page.wait_for_row_in_list_table(TEST_ITEM, 2)
