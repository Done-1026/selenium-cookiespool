import random

import requests

from login import Login
import settings

logined = Login.from_settings(settings)
cookies, url = logined.get_new_cookies()
headers = {
    'user-agent': random.choice(settings.USERAGETNS)
}
resp = requests.get(url, cookies=cookies, headers=headers)


