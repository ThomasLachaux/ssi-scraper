import make_ics
import scrape
import logging as logger
from os import environ
from dotenv import load_dotenv
import argparse as argparse

parser = argparse.ArgumentParser(
                    prog='ssi-scraper',
                    description='This programm scrapes the SSI Master\'s schedule on Moodle and generate corresponding ICS files. You can find the ICS files in folder \'calendars\'.',
                    epilog='First and amazingly created by Thomas de Lachaux.\n Enhanced by Lucien Charleux.')
parser.add_argument('--noscrape', action='store_true', help='skips scraping the XLSX file')
parser.add_argument('filename', nargs='?', help='schedule filename with')
# Logically, this arg should only be used with --noscrape. but the module argparse doesnt provide a simple implementation and I am too lazy to do it.
# Here is the way to do if someone wants to
# https://stackoverflow.com/questions/19414060/argparse-required-argument-y-if-x-is-present

# parser.add_argument('-h', '--help', action='store_true', help='prints this message')
args = parser.parse_args()

load_dotenv()
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

filename='edt.xlsx'
xls=None

if(not args.noscrape): 
    # Change logging level for some verbose modules
    for module in ['selenium.webdriver.remote.remote_connection', 'selenium', 'urllib3.connectionpool']:
        logger.getLogger(module).setLevel(logger.INFO)
    xls = scrape.scrape_xls()
    with open(filename, 'wb') as file:
        file.write(xls)
else:
    if(args.filename):
        filename = args.filename
    with open(filename, 'rb') as file:
        xls = file.read()

for ue in [None, 'gs10', 'gs11', 'gs13', 'gs15', 'gs16', 'gs21']:
    calendar = make_ics.make_ics(xls, ue)

    name = ue
    if not name:
        name = 'all'
    else:
        name = f'except-{ue}'

    with open(f'calendars/ssi-{name}.ics', 'w') as file:
        logger.info(f'Write on calendars/{name}.ics')
        file.write(calendar)
