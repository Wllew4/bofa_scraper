from setuptools import setup

setup(
	name='bofa_scraper',
	version='0.1.1',
	description='Simple Python web-scraper to get personal transaction data from BofA account.',
	url='https://github.com/Wllew4/bofa_scraper',
	author='Wllew4',
	license='GPLv3',
	zip_safe=False,
	packages=['bofa_scraper'],
	install_requires=[
		'selenium'
	]
)