# -*- coding: utf-8 -*-
"""
Functional tests for TDD
"""

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
