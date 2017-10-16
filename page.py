from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from element import BasePageElement
from locators import SearchPageLocators
import time

class TextElement(BasePageElement):
    def __init__(self, *locator):
        self.locator = locator

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def highlight(self, *locator):
        """Highlights (blinks) the element"""
        if self.check_object_exists(*locator):
            element = self.driver.find_element(*locator)
            original_style = element.get_attribute('style')
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                       "background: yellow; border: 2px solid red;")
            time.sleep(3)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                       original_style)


    def check_object_exists(self, *locator):
        """returns true of the object exists, false if it doesn't"""
        time.sleep(1) #give it time to load the object
        try:
            #lambda driver: self.driver.find_element(*locator)
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True


    def click_object(self, *locator):
        """clicks on object"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        for x in range(0, 20):
            try:
                str_error = None
                element.click()

            except Exception as str_error:
                pass

            if str_error:
                time.sleep(1)
            else:
                break

    def double_click_object(self, *locator):
        """double clicks object"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        actionChains = ActionChains(self.driver)
        actionChains.double_click(element).perform()

    def click_object_at_location(self, xoffset, yoffset, *locator):
        """clicks object at x, y offset"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        actionChains = ActionChains(self.driver)
        actionChains.move_to_element_with_offset(element, xoffset, yoffset).click().perform()

    def setChkBox(self, checked, *locator):
        """checks or unchecks a checkbox"""
        element = self.driver.find_element(*locator)
        if (element.get_attribute('checked')):  # if it's checked, only check it if checked is False
            if checked == False:
                element.click()
        else:  # if it's not checked, only check it if checked is True
            if checked == True:
                element.click()


class SearchPage(BasePage):
    search_field = TextElement(*SearchPageLocators.search_field)

    def do_search(self, search_term):
        """Enters search_term and clicks search button"""
        self.search_field = search_term
        self.click_search_btn()

    def click_search_btn(self):
        self.click_object(*SearchPageLocators.search_btn)

    def check_checkbox(self):
        self.setChkBox(True, *SearchPageLocators.ray_ban_checkbox)

    def click_result_item(self, item_no):
        result_item = SearchPageLocators(item_no)
        self.click_object(*result_item.result_item)

    def convert_price_range_string(self, price_string):
        s = price_string.split("-")

        low_price = float(s[0].strip().replace("$ ", "").replace(" ", "."))
        if len(s) > 1:
            high_price = float(s[1].strip().replace("$ ", "").replace(" ", "."))
        else:
            high_price = low_price

        return [low_price, high_price]

    def compare_prices(self, price_range, minimum_price, maximum_price):
        prices = self.convert_price_range_string(price_range)
        low_price = prices[0]
        high_price = prices[1]
        if low_price > maximum_price or high_price < minimum_price:
            return False
        else:
            return True

    def get_matching_items_by_price(self, minimum_price, maximum_price):
        # TODO: put the xpath string in the locators file
        #self.highlight(*SearchPageLocators.results_list)
        #self.highlight(*SearchPageLocators.results_list_xpath)

        matches = 0
        result_elems = self.driver.find_elements_by_xpath("//*[@id='s-results-list-atf']/li")
        for i in range(0, len(result_elems)):
            price_range = self.get_item_price_range(result_elems[i])
            if self.compare_prices(price_range, minimum_price, maximum_price):
                matches += 1

        return matches


    def get_item_price_range(self, result_elem):
            s = result_elem.text
            lines = s.split('\n')
            return lines[1]

