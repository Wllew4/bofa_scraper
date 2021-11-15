# bofa_scraper
Simple Python web-scraper to get personal transaction data from BofA account.

## Set up
1. Clone this repository into your project.
2. Create a `credentials.json` file in the root of your project.
```json
{
  "username": "YourBofaUsername",
  "password": "YourBofaPassword"
}
```
3. Pass the path to `credentials.json` to the constructor of BofaScraper.
```python
from bofa_scraper import BofaScraper
scraper = BofaScraper('credentials.json')
```
4. Make use of the public methods available.

## Security
This repository is intended for PERSONAL USE ONLY to document/calculate finances.
You are free to edit the code for your personal use case.
DO NOT create forks with your account information available.
Make use of .gitignore and be certain you have configured it properly before pushing.
