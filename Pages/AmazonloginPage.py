from base_page import BasePage


class AmazonloginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_ontab(self, tabname):
        self.wait_for_element(f"{tabname}", locator_type="text")
        self.click_element(f"{tabname}", locator_type="text")

    def get_tileofthepage(self):
        return self.driver.title