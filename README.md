# bofa_scraper
Bank of America does not currently have a consumer-facing API for requesting 
balance and transaction data. The goal of this project is to make personal
data accessible to allow for automated budgeting projects.

This project includes a web scraper written in Python using
[Selenium](https://www.selenium.dev/). As such, this project is not capable
of fetching any data that could not be collected by a human in a web browser.
Please always take care to secure your account credentials!

# Getting Started
1. Install the package.
```bash
pip install bofa_scraper
```
2. Add the [Chrome WebDriver](https://chromedriver.chromium.org/downloads)
	to your project's root, or anywhere it is accessible from the 
	command line. You'll also need the associated version of
	[Google Chrome](https://www.google.com/chrome/).
	These binaries are not distributed with the package because they are
	platform dependent.
3. Import the BofaScraper class.
```python
from bofa_scraper import BofAScraper
```
4. Create an instance of the BofAScraper class.
	It is recommended that you store credentials as environment variables.
```python
scraper = BofaScraper(
	'YOUR_BankOfAmerica_ONLINE_ID',
	'YOUR_BankOfAmerica_PASSCODE'
	)
```

# Usage
Using the `scraper: BofAScraper` constructed above:
## Scrape data
Scrape and cache your account data in memory.
```python
scraper.scrape()
```
During the scraping process, you may be asked via the terminal to input a 2fa code.
## Access data
Returns a `list[Account]`.
```python
scraper.getAccounts()
```
### Account:
```python
Account.name		: str				# The name of the account
Account.balance		: float				# The balance of the account
Account.transactions	: list[Transaction]	# A list of this account's recent transactions
```
### Transaction:
```python
Transaction.date	: str				# Date of transaction
Transaction.amount	: float				# Value of transaction
Transaction.desc	: str				# The description of the transaction
```
## Safely close web scraper
```python
scraper.quit()
```

# Security & Licensing
This repository is intended for PERSONAL USE ONLY to document/calculate finances.
It is recommended that you make use of environment variables to secure personal information.

This project is licensed under the GNU General Public License 3.0 (GPLv3).
You are free to use and edit the code for your personal, non-distributed use case.
Any distributed derivative works of this project must be in compliance with
the terms of the GPLv3 license.
Distributed derivative works must be open sourced.
I am not a lawyer, please read the full license included with this project to
understand the totality and specificity of its terms.
