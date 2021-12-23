from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .account import Account
from .transaction import Transaction

class BofAScraper:

	_driver: WebDriver				# web driver
	_credentials = dict()			# username and password
	_data: list[Account] = list()	# data cache

	def __init__(self, online_id: str, passcode: str):
		"""Instantiate web driver"""
		options = webdriver.ChromeOptions()
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		options.headless = True
		options.add_argument('--remote-debugging-port=9222')
		self._driver = Chrome(options=options)
		self._driver.set_window_size(1280, 720)
		self._credentials['username'] = online_id
		self._credentials['password'] = passcode

	def quit(self):
		"""Safely quit web driver"""
		self._driver.quit()

	def getAccounts(self) -> list[Account]:
		"""Retrieve account data"""
		return self._data
    
	def scrape(self):
		"""Scrape and cache account data"""
		self.__login()
		account: WebElement
		if self._driver.current_url == "https://secure.bankofamerica.com/login/sign-in/signOnSuccessRedirect.go":
			self._driver.find_element(By.ID, "btnARContinue").click()
			self._driver.implicitly_wait(2)
			print("input 2fa code: ")
			self._driver.find_element(By.CLASS_NAME, "authcode").send_keys(input())
			self._driver.find_element(By.ID, "yes-recognize").click()
			self._driver.find_element(By.ID, "continue-auth-number").click()
		for account in self._driver.find_elements(By.CLASS_NAME, "AccountItem"):
			acc = Account()
			acc['name'] = self.__get_name(account)
			acc['balance'] = self.__get_balance(account)
			acc['transactions'] = self.__scrape_transactions(account)
			self._data.append(acc)

	def __login(self):
		self._driver.get("https://bankofamerica.com")
		self._driver.find_element(By.ID, "onlineId1").clear()
		self._driver.find_element(By.ID, "onlineId1").send_keys(self._credentials["username"])
		self._driver.find_element(By.ID, "passcode1").clear()
		self._driver.find_element(By.ID, "passcode1").send_keys(self._credentials["password"])
		self._driver.find_element(By.ID, "signIn").click()

	def __get_name(self, account: WebElement) -> str:
		return account.find_element(By.TAG_NAME, "a").get_attribute("innerHTML")

	def __get_balance(self, account: WebElement) -> float:
		return float(
			account.find_element(By.CLASS_NAME, "balanceValue")
			.get_attribute("innerHTML")
			.replace("$", "").replace(",", ""))

	def __scrape_transactions(self, account: WebElement) -> list[Transaction]:
		out: list[Transaction] = list()
		
		url = account.find_element(By.TAG_NAME, "a").get_attribute("href")
		self._driver.execute_script('window.open()')
		self._driver.switch_to.window(self._driver.window_handles[1])
		self._driver.get(url)

		row: WebElement

		for row in self._driver.find_elements(By.CLASS_NAME, "in-transit-record"):
			t = Transaction()
			t["date"] = "processing"
			t["amount"] = float(row.find_element(By.CLASS_NAME, "amount").get_attribute("innerHTML").replace(",",""))
			t["desc"] = row.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML").split("<br>")[0]
			out.append(t)
		for row in self._driver.find_elements(By.CLASS_NAME, "record"):
			t = Transaction()
			t["date"] = row.find_elements(By.TAG_NAME, "span")[1].get_attribute("innerHTML")
			t["amount"] = float(row.find_element(By.CLASS_NAME, "amount").get_attribute("innerHTML").replace(",",""))
			t["desc"] = row.find_element(By.CLASS_NAME, "transTitleForEditDesc").get_attribute("innerHTML")
			out.append(t)

		self._driver.close()
		self._driver.switch_to.window(self._driver.window_handles[0])

		return out