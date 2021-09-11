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

for ue in [None, 'gs15', 'gs16', 'gs21']:
    calendar = make_ics.make_ics(xls, ue)

    name = ue
    if not name:
        name = 'all'
    else:
        name = f'except-{ue}'

    with open(f'calendars/ssi-{name}.ics', 'w') as file:
        logger.info(f'Write on calendars/{name}.ics')
        file.write(calendar)
