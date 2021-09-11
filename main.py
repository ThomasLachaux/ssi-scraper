import make_ics
import filecmp
import scrape
import logging as logger
from os import rename
from dotenv import load_dotenv

old_file_name = 'edt.xlsx'
new_file_name = 'new-edt.xlsx'

load_dotenv()
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

# Change logging level for some verbose modules
for module in ['selenium.webdriver.remote.remote_connection', 'selenium', 'urllib3.connectionpool']:
    logger.getLogger(module).setLevel(logger.INFO)

xls = scrape.scrape_xls()

with open(new_file_name, 'wb') as file:
    file.write(xls)

if not filecmp.cmp(old_file_name, new_file_name):
    logger.warn('Excel changed, create a new ics file')
    make_ics.make_ics(xls)

else:
    logger.info('Excel not changed')

rename(new_file_name, old_file_name)
