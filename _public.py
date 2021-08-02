from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.remote.webelement import WebElement
if TYPE_CHECKING:
    from . import BofaScraper

from .transaction import Transaction

from ._scraping import _login
from ._scraping import _get_account
from ._scraping import _open_account
from ._scraping import _get_transactions
from ._scraping import _scrape_transactions

import json


def get_recent_transactions_by_month(self: BofaScraper, accountName: str) -> dict[str, list[Transaction]]:
    _login(self)
    _open_account(self, accountName)
    return _get_transactions(self)

def get_recent_transactions_as_array(self: BofaScraper, accountName: str) -> list[str]:
    _login(self)
    _open_account(self, accountName)
    return _scrape_transactions(self)

def get_recent_transactions_as_array_json(self: BofaScraper, accountName: str) -> list[str]:
    return json.dumps(get_recent_transactions_as_array(self, accountName))

def get_balance(self: BofaScraper, accountName: str) -> float:
    self._login()
    as_str: str
    self._driver.implicitly_wait(2)
    as_str = _get_account(self, accountName).find_element_by_class_name("balanceValue").get_attribute("innerHTML")
    return float(as_str.replace("$", "").replace(",", ""))

def get_all_balances(self: BofaScraper) -> float:
    self._login()
    self._driver.implicitly_wait(2)
    balance: float = 0
    account: WebElement
    for account in self._driver.find_elements_by_class_name("AccountItem"):
        balance += float(account.find_element_by_class_name("balanceValue").get_attribute("innerHTML").replace("$", "").replace(",", ""))
    return balance