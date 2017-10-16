from selenium.webdriver.common.by import By


class SearchPageLocators(object):
    """A generic class to locate objects on search page"""
    search_field = (By.ID, "twotabsearchtextbox")
    search_btn = (By.XPATH, "//input[@value='Go']")

    ray_ban_checkbox = (By.XPATH, "//input[@name='s-ref-checkbox-Ray-Ban']")

    results_list = (By.ID, "s-results-list-atf")
    results_list_xpath = (By.XPATH, "//*[@id='s-results-list-atf']" )
    price_range = (By.XPATH, "//span[@class='a-offscreen']")

    def __init__(self, result_no):
        # Result cell
        self.result_item = (By.ID, 'result_' + str(result_no))

    low_price_whole = (By.XPATH, "")
    # // *[ @ id = "result_0"] / div / div[3] / div[2] / a / span[2] / span / span[1]

class ItemPage(object):
    """A generic class to locate objects on an item page"""

    back_link = (By.ID, "breadcrumb-back-link")

# TODO:  remove this class!
class WorkspacePageLocators(object):
    """A class for Workspace page locators."""
    add_app_tile = (By.XPATH, "//*[@ng-if='vm.addButton']")  # Tile with + to add an app

    def __init__(self, app_name):
        # App tile -- assign name dynamically
        self.app_tile = (By.XPATH, '//*[@title="' + app_name + '"]')
