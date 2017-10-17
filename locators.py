from selenium.webdriver.common.by import By


class SearchPageLocators(object):
    """A generic class to locate objects on search and results pages"""
    search_field = (By.ID, "twotabsearchtextbox")
    search_btn = (By.XPATH, "//input[@value='Go']")

    ray_ban_checkbox = (By.XPATH, "//input[@name='s-ref-checkbox-Ray-Ban']")

    results_list_id = "s-results-list-atf"
    results_list = (By.ID, results_list_id)

    def __init__(self, result_no):
        # Result cell
        self.result_item = (By.ID, 'result_' + str(result_no))
