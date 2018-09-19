import logging
import time

from selenium import webdriver
import settings

filehandle = logging.FileHandler('log1.log')
streamhandle = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=(filehandle, streamhandle))

options = webdriver.ChromeOptions()
options.KEY = 'goog:chromeOptions'
options.set_headless()
# 创建driver，chromedriver地址为http://127.0.0.1:port,若不指定port则会随机选用空闲端口代码参见selenium.common.service
driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH, chrome_options=options)
#driver.set_window_size(1620, 1020)
driver.get(settings.LOGIN_URL)
#driver.get(r'https://www.baidu.com')
