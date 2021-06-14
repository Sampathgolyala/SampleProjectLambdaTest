import csv
from traceback import print_stack

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.by import By
import logging
import utilities.custom_logger as cl
import time
import os


class BasePage:
    TIMEOUT = 10
    alertWait = 3

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    # Gets By types and returns the value
    def get_by(self, locator_type):
        if locator_type == "id":
            return By.ID
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "text":
            return By.LINK_TEXT
        elif locator_type == "partial_text":
            return By.PARTIAL_LINK_TEXT
        elif locator_type == "tag":
            return By.TAG_NAME
        else:
            self.log.error("Locator type " + locator_type + " not correct/supported")
            return False

    # gets element based on locator and locator type and then return the element
    def find_element(self, locator, locator_type="id"):
        try:
            locator_type = locator_type.lower()
            by = self.get_by(locator_type)
            element = self.driver.find_element(by, locator)
            self.log.info(f"Found element using by_type {locator_type} and locator {locator}")
            return element
        except Exception as f:
            self.log.error(f"element not found using {locator_type} and {locator}")
            return f

    # gets list of elements based on locator and locator type and then return the list
    def find_elements(self, locator, locator_type="id"):
        try:
            locator_type = locator_type.lower()
            by = self.get_by(locator_type)
            element = self.driver.find_elements(by, locator)
            self.log.info(f"Found element using by_type {locator_type} and locator {locator}")
            return element
        except Exception as f:
            self.log.error(f"element not found using {locator_type} and {locator}")
            return f


    def click_element(self, locator, locator_type="id"):
        try:
            element = self.find_element(locator, locator_type)
            element.click()
            self.log.info(f"Clicked on element with locator {locator} and locator_type {locator_type}")
        except Exception as f:
            print(f)
            self.log.error(f"Cannot click on the element with locator {locator} and locator_type {locator_type}")

    # Calls find_element to get element and then send_keys
    def send_data(self, data, locator, locator_type="id"):
        try:
            element = self.find_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f"Sent data {data} to element with locator {locator} and locator_type {locator_type}")
        except Exception as f:
            print(f)
            self.log.error(f"Cannot send data {data} to element with locator {locator} and locator_type {locator_type}")

    def clear_before_sending_data(self, data, locator, locator_type="id"):
        try:
            element = self.find_element(locator, locator_type)
            element.clear()
            element.send_keys(data)
            self.log.info(f"Sent data {data} to element with locator {locator} and locator_type {locator_type}")
        except Exception as f:
            print(f)
            self.log.error(f"Cannot send data {data} to element with locator {locator} and locator_type {locator_type}")

    def send_data_fordropdownvalues(self, data, locator, locator_type="id"):
        try:
            element = self.find_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f"Sent data {data} to element with locator {locator} and locator_type {locator_type}")
        except Exception as f:
            print(f)
            self.log.error(f"Cannot send data {data} to element with locator {locator} and locator_type {locator_type}")

    # Validates if the element is present on the page by locator and locator type and return true or false
    def is_element_present(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            element = self.driver.find_element(by, locator)
            if element is not None:
                self.log.info(f"Found element using by_type {locator_type} and locator {locator}")
                return True
            else:
                self.log.error(f"element not found using {locator_type} and {locator}")
                return False
        except:
            self.log.info(f"element not found using {locator_type} and {locator}")
            return False

    # clears data from field
    def clear_text_filed(self, locator, locator_type="id"):
        try:
            element = self.find_element(locator, locator_type)
            element.clear()
            self.log.info(f"Cleared data from element with locator {locator} and locator_type {locator_type}")
        except Exception as f:
            self.log.error(f"Unable to clear data from element with locator {locator} and locator_type {locator_type}")

    # gets text and returns it's value
    def get_text(self, locator, locator_type="id"):
        try:
            element = self.find_element(locator,locator_type)
            self.log.info(f"Found text {element.text} for element with locator {locator} and locator_type {locator_type}")
            return element.text
        except Exception as f:
            self.log.error(f)
            return f

    def get_text_from_popup(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 50)
            element = wait.until(EC.visibility_of_element_located((by, locator)))
            # elementtext = element.get_text()
            # element = self.find_element(locator,locator_type)
            self.log.info(f"Found text {element.text} for element with locator {locator} and locator_type {locator_type}")
            return element.text
        except Exception as f:
            self.log.error(f)
            return f

    def navigate_to_page_with_url(self, url):
        self.driver.get(url)

    def wait_until_page_with_url_loaded(self, url):
        try:
            page_loaded = EC.url_to_be(url)
            WebDriverWait(self.driver, self.TIMEOUT).until(page_loaded)
        except TimeoutError:
            print("Timed out waiting for page with url - %s to load" % url)
        finally:
            print("Page with url - %s loaded" % url)

    def select_element_from_drop_down(self, text, locator, locator_type="id"):
        try:
            select_element = self.find_element(locator, locator_type)
            select_element.select_by_value(text)
        except Exception as f:
            select_element = Select(self.find_element(locator, locator_type))
            select_element.select_by_visible_text(text)

    def get_all_elements_from_dropdown(self, id):
        select_box = self.driver.find_element_by_id(id)
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            return element.get_attribute("value") is not None

    def are_values_match(self, id, text):
        actual_element = self.driver.find_element_by_id(id).text
        expected_element = text
        if expected_element == actual_element:
            return True
        else:
            print("Values are not matching")

    def alert_accept(self):
        try:
            WebDriverWait(self.driver, self.alertWait).until(EC.alert_is_present(),
                                                             'Timed out waiting for PA creation ' +
                                                             'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def alert_dismiss(self):
        alert_obj = self.driver.switch_to.alert
        alert_obj.dismiss()

    def alert_send_key(self):
        alert_obj = self.driver.switch_to.alert
        alert_obj.send_keys()

    def alert_text(self):
        alert_obj = self.driver.switch_to.alert
        alert_obj.text()

    def implicitly_wait(self):
        self.driver.implicitly_wait(10)

    def implicitly_wait_for_element(self, url, id):
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        self.driver.find_element_by_id(id)

    def close_last_tab(self):
        if (len(self.driver.window_handles) == 2):
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[0])

    # def get_all_rows_from_page(self, xpath):
    #     elements = self.driver.find_elements_by_xpath(xpath)
    #     if (len(elements) > 0):
    #         randomValue = random.randrange(1, len(elements))
    #     value = self.driver.find_element_by_xpath("(// div[ @class ='ui-grid-row ng-scope']//div[1]//div[1]/div)[" + str(randomValue) + "]").text
    #     return value

    #wait for element, once clickble it will return the value
    def wait_for_element(self,locator,locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 50)
            element = wait.until(EC.element_to_be_clickable((by,locator)))
            self.log.info("Element appeared on the web page")
            return element
        except Exception as f:
            print(f)
            self.log.error("Element did not appear on the web page")

    #wait for element extended time, once clickble it will return the value
    def wait_for_element_extended_time(self,locator,locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 100)
            element = wait.until(EC.element_to_be_clickable((by,locator)))
            self.log.info("Element appeared on the web page")
            return element
        except Exception as f:
            print(f)
            self.log.error("Element did not appear on the web page")

     # wait for element, once it's located it will return the value
    def wait_for_located_element(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 30, poll_frequency=1)
            element = wait.until(EC.presence_of_element_located((by, locator)))
            self.log.info("Element appeared on the web page")
            return element
        except Exception as f:
            print(f)
            self.log.error("Element did not appear on the web page")

    def take_screenshot(self, result_message):
        """
        Takes screenshot of the current web pages
        """
        file_name = result_message + str(round(time.time())) + ".png"
        screenshot_directory = "screenshots/"
        file_path = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, file_path)
        destination_directory = os.path.join(current_directory, screenshot_directory)

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            self.driver.save_screenshot(destination_file)
            self.log.info(f"### Screenshot saved to directory {destination_file}")
        except:
            self.log.error("### Exception Occurred")
            print_stack()

    # Validates the page is scrolled down using ActionChains class
    def scroll_down_to_pagebottom(self):
        try:
            action=ActionChains(self.driver)
            action.send_keys(Keys.ARROW_DOWN).perform()
            self.log.info(f"Paged scrolled down successfully")
        except:
            self.log.error("###Page is not scrolled down")

    # Validates the page is scrolled up to the top of the page using JS
    def scroll_to_the_top_of_the_page(self):
        try:
            self.driver.execute_script("window.scrollBy(0,-2100);")
            self.log.info(f"Paged scrolled up successfully")
        except:
            self.log.error("###Page is not scrolled up")

    def doubleclick_ontab(self):
        try:
            N=2
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB * N)
            actions.perform()
            self.log.info(f"double clicked on element down successfully")
        except:
            self.log.error("### not able to double click on element")

    def mouse_hover_movebyoffset(self):
        try:
            action = ActionChains(self.driver)
            action.move_by_offset(10, 500)  # 10px to the right, 20px to bottom
            action.perform()
            self.log.info(f"moved offset down successfully")
        except:
            self.log.error("### not able to move offset")


    def mouse_hover_movetoelement(self,locator, locator_type="id"):
        try:
            action = ActionChains(self.driver)
            webelementtoclick=self.find_element(locator, locator_type)
            action.move_to_element(webelementtoclick).click().perform()
            self.log.info(f"moved offset down successfully")
        except:
            self.log.error("### not able to move offset")

    def get_text_using_mouse_hover(self, locator, locator_type="id"):
        try:
            action = ActionChains(self.driver)
            webelementtoclick = self.find_element(locator, locator_type)
            action.move_to_element(webelementtoclick).perform()
            toolTipElement = self.find_element(locator, locator_type)
            toolTipText = toolTipElement.get_attribute("title")
            self.log.info("able to fetch the tooltip text")
            return toolTipText
        except:
            self.log.error("not able to fetch the tooltip text")

    #Validates the page is scrolled down using javascript executor
    def scroll_down_to_pagewithJavaScriptExecutor(self):
        try:
            self.driver.execute_script("window.scrollTo(0,2000);")
            self.log.info(f"###Page scrolled down to bottom of the page")
        except:
            self.log.error("###Page is not scrolled down")



    # Validates if the element is enabled on the page by locator and locator type and return true or false
    def is_element_enabled(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 50)
            element = wait.until(EC.element_to_be_clickable((by, locator)))
            elementstatus = element.is_enabled()
            if elementstatus is True:
                self.log.info(f"Found element in enable mode using by_type {locator_type} and locator {locator}")
                return True
            else:
                self.log.error(f"element found in disable mode using {locator_type} and {locator}")
                return False
        except:
            self.log.error(f"element not found using {locator_type} and {locator}")
            return False

    def get_tileofthepage(self):
        return self.driver.title

    def get_attributevalue(self, locator, locator_type="id"):
        try:
            element = self.find_element(locator,locator_type)
            elementtext=element.get_attribute("value")
            self.log.info(f"Found text {elementtext} for element with locator {locator} and locator_type {locator_type}")
            return True
        except Exception:
            self.log.error(f"elementtext value not found with locator {locator} and locator_type {locator_type}")
            return False

    def element_not_present(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((by, locator)))
            elementstatus = element.is_displayed()
            self.log.info("Error : Element is found using type " + by +" and locator " +locator)
            return False
        except:
            # self.log.info("element not found using type :" + by +" and locator :" +locator)
            self.log.error(f"element not found using {locator_type} and {locator}")
            return True

    def read_only(self, locator, locator_type="id"):
        locator_type = locator_type.lower()
        by = self.get_by(locator_type)
        elm = self.driver.find_element(by, locator)
        return bool(elm.get_attribute("readonly"))

    def usernameverify_columns_present(self, columnnames, pageortabname, locator, index = 0):
        """Function name - verify_columns_present
        Designed by - mbi-sdas
        Function verifies the columns present in a page or tab
        :param - columnnames : names of the columns in order
                 pageortabname : name of the page or tab where the columns need to be verified
                locator : locator from constants.py page(table level)
                index : index of table where columns need to be verified (when there are more than 1 tabs)
                        [default value : 0]
        :return - Boolean"""
        colmn_names = columnnames.split(";")
        flag = []
        try:
            tables = self.find_elements(locator, locator_type="xpath")
            columns = tables[index].find_elements_by_tag_name("a")
            failed_column = []
            for column in colmn_names:
                i = colmn_names.index(column)
                if columns[i].text.replace('\n', ' ') == column:
                    flag.append(True)
                else:
                    flag.append(False)
                    failed_column.append(column)

            if False not in flag:
                self.log.info(f"Found all the table columns in '{pageortabname}' page/tab")
                return True
            else:
                self.log.error(f"Could not found the table columns ['{failed_column}'] in '{pageortabname}' page/tab")
                return False
        except Exception as e:
            print(e)
            self.log.error(f"Could not found the table columns in '{pageortabname}' page/tab")

    # Validates the double click action performed using ActionChains Class
    def double_click_on_element(self, locator,locator_type="id"):
        try:
            action = ActionChains(self.driver)
            elementtoclick = self.find_element(locator, locator_type)
            action.double_click(elementtoclick).perform()
            self.log.info(f"Double Clicked on element with locator {locator} and locator_type {locator_type}")
        except:
            self.log.error(f"Cannot Double click on the element with locator {locator} and locator_type {locator_type}")

    # Validates the sorting of columns in a table
    def verify_sorting_of_columns(self, locator, locator1,locator_type="id"):
        try:
            columndata = self.find_elements(locator,locator_type)
            listdata = []
            for i in columndata:
                listdata.append(i.text)
                listdata.sort()
            self.wait_for_element(locator1, locator_type="xpath")
            self.click_element(locator1, locator_type="xpath")
            columndata1 = self.find_elements(locator,locator_type)
            flag = []
            for column in columndata1:
                i = columndata1.index(column)
                if column.text == listdata[i]:
                    flag.append(True)
                else:
                    flag.append(False)

            if False not in flag:
                self.log.info(f"column values sorted successfully")
                return True
            else:
                self.log.error(f"column values are not sorted successfully")
                return False
        except Exception as e:
            print(e)
            self.log.error(f"Could not sort the table values in page/tab")

    # Validates the columns present in the table
    def verify_columns_presentintable(self, columnnames, pageortabname,locator,locator_type="id"):
        colmn_names = columnnames.split(";")
        flag = []
        try:
            Columns = self.find_elements(locator,locator_type)
            failed_column = []
            for column in colmn_names:
                i = colmn_names.index(column)
                if column==Columns[i].text:
                    flag.append(True)
                else:
                    flag.append(False)
                    failed_column.append(column)

            if False not in flag:
               self.log.info(f"Found all the table columns in '{pageortabname}' page/tab")
               return True
            else:
               self.log.error(f"Could not found the table columns ['{failed_column}'] in '{pageortabname}' page/tab")
               return False
        except Exception as e:
            print(e)
            self.log.error(f"Could not found the table columns in '{pageortabname}' page/tab")

    def click_choose_file_button_onwindow(self, filename,locator,locator_type="id"):
        try:
            working_directory = os.getcwd()
            path = os.path.join(working_directory, filename)
            self.send_data(path, locator,locator_type)
            self.log.info(f"Able to add file using path {filename}")
        except Exception as f:
            self.log.error(f)

    def write_rowvalues_tocsv(self, itemnumber, storenumber, quantity, filename):
        global get_itemnumber
        global get_storenumber
        get_itemnumber = itemnumber
        get_storenumber = storenumber
        working_directory = os.getcwd()
        path = os.path.join(working_directory, filename)
        file = open(path, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(['', itemnumber])
        writer.writerow([storenumber, quantity])
        file.close()

    # Validates if list of webelements present on the page by locator and locator type and return true or false
    def is_element_list_present(self, locator, locator_type="id"):
        try:
            by = self.get_by(locator_type)
            element = self.driver.find_elements(by, locator)
            if len(element) != 0:
                self.log.info(f"Found elements using by_type {locator_type} and locator {locator}")
                return True
            else:
                self.log.error(f"elements not found using {locator_type} and {locator}")
                return False
        except:
            self.log.info(f"elements not found using {locator_type} and {locator}")
            return False