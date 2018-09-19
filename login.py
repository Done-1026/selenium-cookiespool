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

stream = logging.StreamHandler()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=(logging.StreamHandler(), logging.FileHandler('login.log')))
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
        driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH, chrome_options=self.options)
        driver.get(settings.LOGIN_URL)
        # self.driver.implicitly_wait(20)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)
        try:
            tag_username = wait.until(ES.presence_of_element_located((By.ID, 'loginname')))
        except TimeoutException as e:
            logger.info("Can't find the tags of username!")
            raise Exception('Homepage Timeout:', e)
        tag_password = driver.find_element_by_xpath(r'//input[@type="password"]')
        tag_login_btn = driver.find_element_by_xpath(r'//div[@class="info_list login_btn"]/a')
        tag_username.clear()
        tag_password.clear()
        tag_username.send_keys(username)
        tag_password.send_keys(password)
        time.sleep(0.5)
        tag_login_btn.click()
        try:
            skip = wait.until(ES.url_changes(settings.LOGIN_URL))
        except TimeoutException as e:
            logger.info("Login fail!Page doesn't skip!")
            raise Exception('Logining page Timeout:', e)
        if skip:
            set_cookies = driver.get_cookies()
            cookies = {}
            for cookie in set_cookies:
                cookies[cookie['name']] = cookie['value']
            self.cookie_pool.append(cookies)

    def refresh(self):
        tds = []
        for k,v in settings.ACCOUTS.items():
            td = threading.Thread(target=self.get_cookies, args=(k,v))
            tds.append(td)
        for t in tds:
            t.start()
        for t in tds:
            t.join()


if __name__ == '__main__':
    cookie = CookiePool()
