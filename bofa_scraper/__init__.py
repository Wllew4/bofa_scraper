from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from .util import Log, Timeout
from .account import Account
from .scrape_session import ScrapeSession

class BofAScraper:
	creds = dict()
	driver: webdriver.Firefox
	logged_in = False

	def __init__(self, online_id: str, passcode: str, timeout_duration=5, verbose=True, headless=True):
		self.creds["id"] = online_id
		self.creds["passcode"] = passcode
		Log.set_verbose(verbose)
		Timeout.set_duration(timeout_duration)

		Log.log("Initializing web driver...")
		options = webdriver.FirefoxOptions()
		options.headless = headless
		self.driver = webdriver.Firefox(options=options)
		self.driver.set_window_size(1280, 972)
		self.driver.get("https://www.bankofamerica.com/")
		Timeout.timeout()
		Log.log("Initialized web driver")
	
	def quit(self):
		self.driver.quit()

	def open_account(self, account: Account) -> ScrapeSession:
		return ScrapeSession(self.driver, account)

	def get_accounts(self) -> List[Account]:
		Log.log("Fetching accounts...")
		out = []
		if not self.logged_in:
			Log.log("Not signed in")
		else:
			i = 0
			for account_element in self.driver.find_elements(By.CLASS_NAME, "AccountItem"):
				account = Account(account_element)
				Log.log("Found account: %s" % account.get_name())
				out.append(account)
				i = i + 1
			Log.log("Found %d accounts" % i)
		return out

	def login(self):
		Log.log('Logging in...')
		self.driver.find_element(By.ID, "onlineId1").send_keys(self.creds["id"])
		self.driver.find_element(By.ID, "passcode1").send_keys(self.creds["passcode"])
		self.driver.find_element(By.ID, "signIn").click()
		Timeout.timeout()

		# 2fa
		if self.driver.current_url == "https://secure.bankofamerica.com/login/sign-in/signOnSuccessRedirect.go":
			Log.log('2fa required')
			self.driver.find_element(By.ID, "btnARContinue").click()
			print("input 2fa code: ")
			self.driver.find_element(By.CLASS_NAME, "authcode").send_keys(input())
			self.driver.find_element(By.ID, "yes-recognize").click()
			self.driver.find_element(By.ID, "continue-auth-number").click()
			Timeout.timeout()

		if self.driver.current_url.startswith('https://secure.bankofamerica.com/myaccounts/'):
			Log.log('Sign in success!')
			self.logged_in = True
		else:
			Log.log('Sign in failed')
			self.logged_in = False