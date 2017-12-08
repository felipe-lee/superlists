# -*- coding: utf-8 -*-
"""
Helpers for functional tests
"""
from selenium import webdriver


def get_webdriver():
    """
    Setup a webdriver
    """
    return webdriver.Chrome()
    # return webdriver.Firefox()
