from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .account import Account, Transaction
from .util import Log, Timeout

class ScrapeSession:
	driver: webdriver.Firefox
	account: Account

	def __init__(self, driver: webdriver.Firefox, account: Account):
		self.driver = driver
		self.account = account

		Log.log('Starting scraping session for account %s' % account.get_name())
		url = self.account.get_element().find_element(By.TAG_NAME, "a").get_attribute("href")
		self.driver.execute_script('window.open()')
		self.driver.switch_to.window(self.driver.window_handles[1])
		self.driver.get(url)
		Timeout.timeout()
		Log.log('Tab opened for account %s' % account.get_name())

	def close(self):
		Log.log('Closing tab for account %s...' % self.account.get_name())
		self.driver.close()
		self.driver.switch_to.window(self.driver.window_handles[0])
		Log.log('Closed')

	def scrape_transactions(self):
		Log.log('Scraping transactions for account %s...' % self.account.get_name())
		i: int = 0
		out: list[Transaction] = []
		row: WebElement
		for row in self.driver.find_elements(By.CLASS_NAME, "activity-row"):
			transaction = Transaction()
			transaction.amount = float(row.find_element(By.CLASS_NAME, "amount-cell").text.replace(",","").replace("$",""))
			transaction.date = row.find_element(By.CLASS_NAME, "date-cell").text
			transaction.desc = row.find_element(By.CLASS_NAME, "desc-cell").text.replace("\nView/Edit","")
			transaction.type = row.find_element(By.CLASS_NAME, "type-cell").text
			transaction.uuid = row.get_attribute("class").split(" ")[1]

			out.append(transaction)
			i = i + 1
		Log.log('Found %d transactions on account %s' % (i, self.account.get_name()))
		self.account.set_transactions(out)
		return self

	def load_more_transactions(self):
		Log.log('Loading more transactions in account %s...' % self.account.get_name())
		view_more = self.driver.find_element(By.CLASS_NAME, "view-more-transactions")
		self.driver.execute_script("arguments[0].click();", view_more)
		Timeout.timeout()
		Log.log('Loaded more transactions in account %s' % self.account.get_name())
		return self
