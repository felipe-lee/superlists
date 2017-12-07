# -*- coding: utf-8 -*-
"""
Base tests for lists app
"""
from django.test import TestCase


class SmokeTest(TestCase):
    
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
