import os
import time
from selenium import webdriver
from selenium.webdriver import chrome, DesiredCapabilities
from configparser import ConfigParser

from selenium.webdriver.ie.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import constants

config = ConfigParser()
config.read("./inputs/Config.cfg")
caps = {}


def before_all(context):
    # print(context)
    capability = {"brower": "path"}
    browser = constants.Browsers
    path = constants.WEBDRIVER_PATH
    if browser == "firefox":
        context.driver = webdriver.Firefox(path)
    elif browser == "chrome":
        context.driver = webdriver.Chrome(ChromeDriverManager().install())
        # context.driver = webdriver.Chrome(path)
    elif browser == "ie":
        context.driver = webdriver.Ie(path)
    else:
        raise ValueError("Unrecognized browser %s" % browser)
    context.driver.get(config.get("Environments", "url"))
    context.driver.maximize_window()
    context.driver.implicitly_wait(3)


def after_all(context):
    context.driver.quit()
#
# def before_all(context):
#     # config = ConfigParser()
#     # config.read("./inputs/Config.cfg")
# 
#     if os.getenv('LT_USERNAME', 0) == 0:
#         #context.driver.get(config.get("Environments", "url"))
#         context.user_name = config.get('Environment', 'LUserName')
#     if os.getenv('LT_APPKEY', 0) == 0:
#         context.app_key = config.get('Environment', 'AppKey')
#     if os.getenv('LT_OPERATING_SYSTEM', 0) == 0:
#         context.os = config.get('Environment', 'OS')
#     if os.getenv('LT_BROWSER', 0) == 0:
#         context.browser = config.get('Environment', 'Browser')
#     if os.getenv('LT_BROWSER_VERSION', 0) == 0:
#         context.browser_version = config.get('Environment', 'BrowserVersion')
# 
#     remote_url = "https://" + context.user_name + ":" + context.app_key + "@hub.lambdatest.com/wd/hub"
#     caps['name'] = "Behave Sample Test"
#     caps['build'] = "Behave Selenium Sample"
#     caps['browserName'] = context.browser
#     caps['version'] = context.browser_version
#     caps['platform'] = context.os
#     caps['tunnel']=True
#     print(caps)
#     print(remote_url)
#     context.driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=caps)
#     context.driver.get(config.get("Environments", "url"))
#     context.driver.maximize_window()
#     context.driver.implicitly_wait(3)
#     context.driver.find_element_by_css_selector(constants.USERNAME).send_keys(config.get("Logincredentials", "username"))
#     context.driver.find_element_by_xpath(constants.SUBMITBUTON).click()
#     context.driver.find_element_by_css_selector(constants.PASSWORD).send_keys(config.get("Logincredentials", "password"))
#     context.driver.find_element_by_xpath(constants.SUBMITBUTON).click()
