from typing import TypedDict
from .transaction import Transaction

class Account(TypedDict):
	name: str
	balance: float
	transactions: list[Transaction]