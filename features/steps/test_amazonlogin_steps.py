from behave import *

from Pages.AmazonloginPage import AmazonloginPage
from utilities.test_status import TestStatus


@given('I click "{tabname}" link')
@when('I click "{tabname}" link')
def step_impl(context, tabname):
    amazonpage = AmazonloginPage(context.driver)
    amazonpage.click_ontab(tabname)


@then('I verify the title of the page as "{titlepage}"')
def step_impl(context, titlepage):
    amazonpage = AmazonloginPage(context.driver)
    tc = TestStatus(context.driver)
    titleofthepage = amazonpage.get_tileofthepage()
    if titleofthepage == titlepage:
        status = True
    else:
        status = False

    tc.mark_final("verify the title of the page", status, f"{titlepage} is verified  successfully")
