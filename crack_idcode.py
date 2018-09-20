
from selenium import webdriver
from selenium.webdriver import ActionChains

import settings

def simple_slider(driver, tags):
    actions = ActionChains(driver)
    actions.drag_and_drop_by_offset(tags, 300, 0)
    actions.perform()

