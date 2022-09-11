from typing import List, TypedDict
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class Transaction:
	amount: float
	date: str
	desc: str
	type: str
	uuid: str

class Account:
	__name: str
	__balance: float
	__transactions: List[Transaction]
	__element: WebElement

	def __init__(self, account_element: WebElement):
		self.__element = account_element
		self.__name = self.__element.find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
		self.__balance = float(
			account_element.find_element(By.CLASS_NAME, "balanceValue")
			.get_attribute("innerHTML")
			.replace("$", "").replace(",", ""))
		self.__transactions = []
	
	def get_name		(self)	-> str:					return self.__name
	def get_balance		(self)	-> float:				return self.__balance
	def get_transactions(self)	-> List[Transaction]:	return self.__transactions
	def get_element		(self)	-> WebElement:			return self.__element

	def set_transactions(self, transactions: List[Transaction]):
		self.__transactions = transactions
