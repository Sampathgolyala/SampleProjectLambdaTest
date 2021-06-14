"""
@package utilities

CheckPoint class implementation
It provides functionality to assert the result

Example:
    self.check_point.markFinal("Test Name", result, "Message")
"""
import logging
import utilities.custom_logger as cl
from base_page import BasePage
from traceback import print_stack

class TestStatus(BasePage):
    logger = cl.custom_logger(logging.INFO)

    def __init__(self, driver):
        """
        Inits CheckPoint class
        """
        super(TestStatus, self).__init__(driver)
        self.result_list = []

    def set_result(self, result, result_message):
        try:
            if result is not None:
                if result:
                    self.result_list.append("PASS")
                    self.logger.info(f"### VERIFICATION SUCCESSFUL : {result_message}")
                else:
                    self.result_list.append("FAIL")
                    self.logger.error(f"### VERIFICATION FAILED : {result_message}")
                    self.take_screenshot(result_message)
            else:
                self.result_list.append("FAIL")
                self.logger.error(f"### VERIFICATION WAS NOT SETUP CORRECTLY : {result_message}")
                self.take_screenshot(result_message)
        except:
            self.result_list.append("FAIL")
            self.logger.error(f"### EXCEPTION ERROR")
            self.take_screenshot(result_message)
            print_stack()


    def mark(self, result, result_message):
        """
        Mark the result of the verification point in a test case
        """
        self.set_result(result,result_message)


    def mark_final(self,test_name,result,result_message):
        """
            Mark the final result of the verification point in a test case
            This needs to be called at least once in a test case
            This should be final test status of the test case
        """
        self.set_result(result, result_message)
        if "FAIL" in self.result_list:
            self.logger.error(f"{test_name} ### TEST FAILED")
            self.result_list.clear()
            assert True == False
        else:
            self.logger.info(f"{test_name} ### TEST SUCCESSFUL")
            self.result_list.clear()
            assert True == True

