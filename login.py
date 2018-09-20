import time
import logging
import threading

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import settings
import crack_idcode

crack = {'simple_slider': crack_idcode.simple_slider}

stream = logging.StreamHandler()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=(logging.StreamHandler(), logging.FileHandler('login.log', mode=settings.LOG_MODE)))
logger = logging.getLogger(__name__)


class CookiePool:
    def __init__(self):
        self.cookie_pool = []
        self.set_options()
        self.refresh()

    def set_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.headless = True if settings.HEADLESS else False
        logger.info('ChromeOptions:%s' % self.options.arguments)

    def get_cookies(self, username, password):
        self.driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH, chrome_options=self.options)
        self.driver.set_window_size(1920, 1200)
        self.driver.get(settings.LOGIN_URL)
        # self.self.driver.implicitly_wait(20)
        wait = WebDriverWait(self.driver, 20)
        password_by, password_value = settings.LOGIN_ELEMENT.get('password').values()
        login_btn_by, login_btn_value = settings.LOGIN_ELEMENT.get('login_button').values()
        try:
            tag_username = wait.until(
                ES.presence_of_element_located(tuple(settings.LOGIN_ELEMENT.get('username').values())))
            tag_password = self.driver.find_element(password_by, password_value)
            tag_login_btn = self.driver.find_element(login_btn_by, login_btn_value)
        except TimeoutException as e:
            logger.info("Can't find the tags of username!")
            raise Exception('Homepage Timeout:', e)
        tag_username.clear()
        tag_password.clear()
        tag_username.send_keys(username)
        tag_password.send_keys(password)
        time.sleep(0.5)
        tag_login_btn.click()
        self.driver.implicitly_wait(20)
        if not ES.url_changes(settings.LOGIN_URL)(self.driver):
            tag_idcode_by, tag_idcode_value = settings.LOGIN_ELEMENT.get(settings.IDCODE_TYPE)
            tag_idcode = self.driver.find_element(tag_idcode_by, tag_idcode_value)
            crack_func = crack.get(settings.IDCODE_CRACK.get(settings.IDCODE_TYPE))
            crack_func(self.driver, tag_idcode)
            time.sleep(0.5)
            tag_login_btn.click()
        set_cookies = self.driver.get_cookies()
        cookies = {}
        for cookie in set_cookies:
            cookies[cookie['name']] = cookie['value']
        self.cookie_pool.append(cookies)

    def refresh(self):
        tds = []
        for k, v in settings.ACCOUTS.items():
            td = threading.Thread(target=self.get_cookies, args=(k, v))
            tds.append(td)
        for t in tds:
            t.start()
        for t in tds:
            t.join()


if __name__ == '__main__':
    cookie = CookiePool()
