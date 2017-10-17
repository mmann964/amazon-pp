import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from element import BasePageElement
from locators import SearchPageLocators


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
        time.sleep(1)   # give it time to load the object
        try:
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
        action_chains = ActionChains(self.driver)
        action_chains.double_click(element).perform()

    def click_object_at_location(self, xoffset, yoffset, *locator):
        """clicks object at x, y offset"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element_with_offset(element, xoffset, yoffset).click().perform()

    def set_check_box(self, checked, *locator):
        """checks or unchecks a checkbox"""
        element = self.driver.find_element(*locator)
        if element.get_attribute('checked'):  # if it's checked, only check it if checked is False
            if not checked:
                element.click()
        else:  # if it's not checked, only check it if checked is True
            if checked:
                element.click()


class SearchPage(BasePage):
    search_field = TextElement(*SearchPageLocators.search_field)

    def do_search(self, search_term):
        """Enters search_term and clicks search button"""
        self.search_field = search_term
        self.click_search_btn()

    def click_search_btn(self):
        """clicks the search button"""
        self.click_object(*SearchPageLocators.search_btn)

    def check_rayban_checkbox(self):
        """checks the checkbox for the Ray-Ban brand"""
        self.set_check_box(True, *SearchPageLocators.ray_ban_checkbox)

    def click_result_item(self, item_no):
        """clicks on the given item in the result list"""
        result_item = SearchPageLocators(item_no)
        self.click_object(*result_item.result_item)

    def convert_price_range_string(self, price_string):
        """returns a list with the low and high prices from the given string
            if only one price is in the string, the low and high prices are the same"""

        s = price_string.split("-")

        low_price = float(s[0].strip().replace("$ ", "").replace(" ", "."))
        if len(s) > 1:
            high_price = float(s[1].strip().replace("$ ", "").replace(" ", "."))
        else:
            high_price = low_price

        return [low_price, high_price]

    def compare_prices(self, price_range, minimum_price, maximum_price):
        """returns True if the price range of the item is
        within the minimum and maximum prices; otherwise returns False"""
        prices = self.convert_price_range_string(price_range)
        low_price = prices[0]
        high_price = prices[1]
        if low_price > maximum_price or high_price < minimum_price:
            return False
        else:
            return True

    def get_matching_items_by_price(self, minimum_price, maximum_price):
        """returns the number of items on the page with a price range between the given minimum and maximum prices"""
        matches = 0
        result_elems = self.driver.find_elements_by_xpath("//*[@id='" + SearchPageLocators.results_list_id + "']/li")
        for i in range(0, len(result_elems)):
            price_range = self.get_item_price_range(result_elems[i])
            if self.compare_prices(price_range, minimum_price, maximum_price):
                matches += 1

        return matches

    def get_item_price_range(self, result_elem):
        """returns a string with the price range for an element"""
        s = result_elem.text
        lines = s.split('\n')
        for line in lines:  # look for the line starting with '$ '
            if line[0:2] == "$ ":
                return line
        return "$ 0 00"     # if you've gotten this far, it couldn't find pricing info.  Return string with $0.00

