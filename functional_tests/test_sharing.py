# -*- coding: utf-8 -*-
"""
FTs to test sharing lists
"""
from .base import FunctionalTest
from .helpers import get_webdriver

TEST_EMAIL_1 = 'emily@knightsofhaven.net'
TEST_EMAIL_2 = 'oniciferous@knightsofhaven.net'


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

        self.add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@knightsofhaven.net')
