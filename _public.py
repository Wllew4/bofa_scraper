from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import BofaScraper

from .transaction import Transaction

from ._scraping import _login
from ._scraping import _get_account
from ._scraping import _open_account
from ._scraping import _get_transactions


def get_recent_transactions(self: BofaScraper) -> dict[str, list[Transaction]]:
    _login(self)
    _open_account(self)
    return _get_transactions(self)


def get_balance(self: BofaScraper) -> float:
    self._login()
    as_str: str
    self.driver.implicitly_wait(2)
    as_str = _get_account(self).find_element_by_class_name("balanceValue").get_attribute("innerHTML")
    return float(as_str.replace("$", "").replace(",", ""))