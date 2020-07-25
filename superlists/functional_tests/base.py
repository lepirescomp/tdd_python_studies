from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os


MAX_WAIT = 3


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_url = os.environ.get("STAGING_SERVER")

        if staging_url:
            self.live_server_url = "http://" + staging_url

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def find_element_in_row(self, tag, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id(tag)
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(
                    text, [row.text for row in rows], f"{text} is not on list"
                )
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
