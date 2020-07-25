from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @unittest.skip
    def test_cannot_add_empty_list_items(self):
        pass
