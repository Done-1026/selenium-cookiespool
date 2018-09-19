import time
import logging
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 键盘操作
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标操作
from selenium.webdriver.chrome.options import Options

import settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=(logging.StreamHandler, logging.FileHandler))
logger = logging.getLogger(__name__)


class CookiePool:
    def __init__(self):
        self.cookie_pool = []

    def new_driver(self):
        options = webdriver.ChromeOptions()
        if settings.HEADLESS:
            options.headless = True
        logger.info('ChromeOptions:%s' % options.arguments)
        return webdriver.Chrome(executable_path=settings.DRIVER_PATH, chrome_options=options)

    def get_cookies(self, driver):
        driver.get(settings.LOGIN_URL)
        # self.driver.implicitly_wait(20)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)
        try:
            username = wait.until(ES.presence_of_element_located((By.ID, 'loginname')))
        except TimeoutException as e:
            raise Exception('Timeout:  ', e)
        password = driver.find_element_by_xpath(r'//input[@type="password"]')
        login = driver.find_element_by_xpath(r'//div[@class="info_list login_btn"]/a')
        username.clear()
        password.clear()
        for k, v in settings.ACCOUTS.items():
            username.send_keys(k)
            password.send_keys(v)
            time.sleep(0.5)
            login.click()
            set_cookies = driver.get_cookies()
            cookies = {}
            for cookie in set_cookies:
                cookies[cookie['name']] = cookie['value']
            self.cookie_pool.append(cookies)


if __name__ == '__main__':
    cookie = CookiePool()
