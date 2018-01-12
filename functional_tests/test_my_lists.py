# -*- coding: utf-8 -*-
"""
FTs for user lists
"""
from django.conf import settings
from django.contrib.auth import get_user_model

from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

User = get_user_model()
TEST_EMAIL = 'emily@knightsofhaven.net'


class MyListsTest(FunctionalTest):
    
    def create_pre_authenticated_session(self, email):
        """
        Creates session to avoid having to do this for every FT
        """
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        # # to set a cookie we need to first visit the domain. 404 pages load teh quickest!
        self.browser.get(f'{self.live_server_url}/404/')
        
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
    
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.browser.get(self.live_server_url)
        
        self.wait_to_be_logged_out(TEST_EMAIL)
        
        # Emily is a logged-in user
        self.create_pre_authenticated_session(TEST_EMAIL)
        
        self.browser.get(self.live_server_url)
        
        self.wait_to_be_logged_in(TEST_EMAIL)
