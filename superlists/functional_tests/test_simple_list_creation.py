from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from functional_tests.base import FunctionalTest


class NewVisitor(FunctionalTest):
    def test_can_start_a_list(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)

        header_element = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_element)

        input_box = self.browser.find_element_by_id("id_new_item")
        placeholder = input_box.get_attribute("placeholder")
        self.assertEqual(placeholder, "Enter a to-do item")

        input_box.send_keys("buy food")
        input_box.send_keys(Keys.ENTER)

        self.find_element_in_row("id_list_table", "1: buy food")

        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("buy forks")
        input_box.send_keys(Keys.ENTER)

        self.find_element_in_row("id_list_table", "2: buy forks")

        self.find_element_in_row("id_list_table", "1: buy food")
        self.find_element_in_row("id_list_table", "2: buy forks")

    def test_multiple_list(self):
        self.browser.get(self.live_server_url)

        input_box = self.browser.find_element_by_id("id_new_item")

        input_box.send_keys("buy food")
        input_box.send_keys(Keys.ENTER)

        self.find_element_in_row("id_list_table", "1: buy food")

        edith_url = self.browser.current_url
        self.assertRegex(edith_url, "/lists/.+")

        ## Begin of Francy's test
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("1: buy food", page_text)
        self.assertNotIn("2: buy forks", page_text)

        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("orange")
        input_box.send_keys(Keys.ENTER)

        self.find_element_in_row("id_list_table", "1: orange")

        francys_url = self.browser.current_url
        self.assertRegex(francys_url, "/lists/.+")
        self.assertNotEqual(francys_url, edith_url)

        francys_page = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("1: buy food", francys_page)
        self.assertIn("1: orange", francys_page)
