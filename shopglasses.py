#!/usr/bin/python

import time
import unittest
import page
from selenium import webdriver

url = "http://www.amazon.com"
searchTerm = "glasses"
brand = "Ray-Ban"
min_price = 80
max_price = 150

class SearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.get(url)

    def test_01(self):
        """Search for glasses with brand=Ray-ban"""
        search_page = page.SearchPage(self.driver)

        search_page.do_search(searchTerm)
        search_page.check_checkbox()

        #search_page.click_result_item(0)
        matches = search_page.get_matching_items_by_price(min_price, max_price)
        print "The number of Ray-ban glasses between ${} and ${} is:  {}".format(min_price, max_price, matches)
        time.sleep(5)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
