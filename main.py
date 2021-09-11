import make_ics
import scrape
import logging as logger
from os import rename
from dotenv import load_dotenv

load_dotenv()
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

# Change logging level for some verbose modules
for module in ['selenium.webdriver.remote.remote_connection', 'selenium', 'urllib3.connectionpool']:
    logger.getLogger(module).setLevel(logger.INFO)

xls = scrape.scrape_xls()

with open('edt.xlsx', 'wb') as file:
    file.write(xls)

make_ics.make_ics(xls)
