# bofa_scraper
![version](https://img.shields.io/pypi/v/bofa_scraper?color=blue)
![downloads](https://img.shields.io/pypi/dm/bofa_scraper?color=blue)

Bank of America does not currently have a consumer-facing API for requesting 
balance and transaction data. The goal of this project is to make personal
data accessible to allow for automated budgeting projects.

This project includes a web scraper written in [Python](https://www.python.org/) using
[Selenium](https://www.selenium.dev/). As such, this project is not capable
of fetching any data that could not be collected by a human in a web browser.
**Please always take care to secure your account credentials!**


# Getting Started
1. Install the package.
```
pip install bofa_scraper
```
2. Install Firefox
3. Download the [GeckoDriver](https://github.com/mozilla/geckodriver/releases) binary, and add to your PATH.


# Usage
**NOTE: API has been reworked since v0**

Import and initialize
```python
from bofa_scraper import BofAScraper # Import the package

scraper = BofAScraper(
	'YOUR_BankOfAmerica_ONLINE_ID',
	'YOUR_BankOfAmerica_PASSCODE',
	timeout_duration=5, # Timeout to allow for page loads, defaults to 5s
	headless=True,		# Optional, defaults to True
	verbose=True,		# Optional, defaults to True
)

scraper.login() # Log in
```

Start scraping
```python
# Fetch a list of accounts
# Transaction data is not automatically populated
accounts = scraper.get_accounts()
accounts[0].get_name()		# See account name
accounts[0].get_balance()	# See account balance

# Start a scraping session for an account
(
	scraper.open_account(accounts[0])	# Start session
		.scrape_transactions()			# Scrape visible transactions
		.load_more_transactions()		# Load more transactions
		.scrape_transactions()			# Scrape new and re-scrape old transactions
		.close()						# Close session
)

# Dictionary populated with transactions
transactions = accounts[0].get_transactions()
# transaction info
transactions[0].amount
transactions[0].date
transactions[0].desc
transactions[0].type
transactions[0].uuid
```

Clean up
```python
scraper.quit()
```


# Security & Licensing
This project is licensed under the GNU General Public License 3.0 (GPLv3).

This project is intended for PERSONAL USE ONLY to document/calculate finances.
**Please take security into account when handling financial credentials.**
