from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
import json

class BofaScraper:
    def __init__(self, credentials_file: str):
        self.driver = Chrome()
        self.driver.set_window_position(-10000, 0)
        self.driver.set_window_size(1280, 720)
        self.credentials = json.loads(
            open(credentials_file, "r")
            .read())

    def __del__(self):
        self.driver.close()

    driver: WebDriver
    credentials: dict

    from ._public import get_recent_transactions
    from ._public import get_balance

    from ._scraping import _login
    from ._scraping import _get_account
    from ._scraping import _open_account
    from ._scraping import _get_transactions