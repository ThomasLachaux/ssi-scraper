from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import environ
import requests
import logging


logger = logging.getLogger(__name__)


def scrape_xls():
    logger.debug('Start web browser')
    driver = webdriver.Remote(command_executor=environ.get('COMMAND_EXECUTOR'),
                              desired_capabilities=DesiredCapabilities.CHROME)
    logger.debug('Authenticate to cas')
    driver.get(
        'https://cas.utt.fr/cas/login?service=https%3A%2F%2Fmoodle.utt.fr%2Flogin%2Findex.php%3FauthCAS%3DCAS')

    username = driver.find_element_by_id('username')
    username.send_keys(environ.get('ENT_USERNAME'))

    password = driver.find_element_by_id('password')
    password.send_keys(environ.get('ENT_PASSWORD'))

    logger.debug('Submit the login form')
    submit = driver.find_element_by_class_name('btn-submit')
    submit.click()

    driver.set_page_load_timeout(30)
    logger.debug('Callback fully loaded, get session cookies and quit')
    cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Ignore TLS errors because the DH Key on the server is too small
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    request = session.get(
        'https://moodle.utt.fr/mod/resource/view.php?id=58119&redirect=1')

    logger.info('Excel successfully downloaded')

    return request.content
