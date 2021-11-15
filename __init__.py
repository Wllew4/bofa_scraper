from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import json

from .account import Account
from.transaction import Transaction

class BofaScraper:

    _driver: WebDriver
    _credentials: dict
    _debug: bool

    _data: list[Account] = list()

    def __init__(self, credentials_file: str, debug: bool):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # options.headless = True
        options.add_argument('--remote-debugging-port=9222')
        self._driver = Chrome(options=options)
        self._debug = debug
        self._driver.set_window_size(1280, 720)
        self._credentials = json.loads(
            open(credentials_file, "r")
            .read())

    def __del__(self):
        self._driver.quit()

        
    def getAccounts(self) -> list[Account]:
        return self._data
    

    def scrape(self):
        self.__login()
        account: WebElement
        print(self._driver.current_url)
        # if self._driver.current_url == "https://secure.bankofamerica.com/login/sign-in/signOnSuccessRedirect.go":
        #     self._driver.find_element_by_id("btnARContinue").click()
        #     self._driver.implicitly_wait(2)
        #     print("input 2fa code: ")
        #     self._driver.find_element_by_class_name("authcode").send_keys(input())
        #     self._driver.find_element_by_id("yes-recognize").click()
        #     print(self._driver.find_element_by_id("continue-auth-number"))
        #     self._driver.find_element_by_id("continue-auth-number").click()
        for account in self._driver.find_elements_by_class_name("AccountItem"):
            acc = Account()
            acc.name = self.__get_name(account)
            acc.balance = self.__get_balance(account)
            acc.transactions = self.__scrape_transactions(account)
            self._data.append(acc)

    def __login(self):
        self._driver.get("https://bankofamerica.com")
        self._driver.find_element_by_id("onlineId1").clear()
        self._driver.find_element_by_id("onlineId1").send_keys(self._credentials["username"])
        self._driver.find_element_by_id("passcode1").clear()
        self._driver.find_element_by_id("passcode1").send_keys(self._credentials["password"])
        self._driver.find_element_by_id("signIn").click()

    def __get_name(self, account: WebElement) -> str:
        return account.find_element_by_tag_name("a").get_attribute("innerHTML")

    def __get_balance(self, account: WebElement) -> float:
        return float(
            account.find_element_by_class_name("balanceValue")
            .get_attribute("innerHTML")
            .replace("$", "").replace(",", ""))

    def __scrape_transactions(self, account: WebElement) -> list[Transaction]:
        out: list[Transaction] = list()
        
        url = account.find_element_by_tag_name("a").get_attribute("href")
        self._driver.execute_script('window.open()')
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get(url)

        row: WebElement
        for row in self._driver.find_elements_by_class_name("in-transit-record"):
            t = Transaction()
            t["date"] = "processing"
            t["amount"] = float(row.find_element_by_class_name("amount").get_attribute("innerHTML").replace(",",""))
            t["desc"] = row.find_elements_by_tag_name("td")[1].get_attribute("innerHTML").split("<br>")[0]
            out.append(t)
        for row in self._driver.find_elements_by_class_name("record"):
            t = Transaction()
            t["date"] = row.find_elements_by_tag_name("span")[1].get_attribute("innerHTML")
            t["amount"] = float(row.find_element_by_class_name("amount").get_attribute("innerHTML").replace(",",""))
            t["desc"] = row.find_element_by_class_name("transTitleForEditDesc").get_attribute("innerHTML")
            out.append(t)

        self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[0])

        return out