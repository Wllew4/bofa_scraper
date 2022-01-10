from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
	name='bofa_scraper',
	version='0.1.3',
	description='Simple Python web-scraper to get personal transaction data from BofA account.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Wllew4/bofa_scraper',
	author='Wllew4',
	license='GPLv3',
	zip_safe=False,
	packages=['bofa_scraper'],
	install_requires=[
		'selenium'
	]
)