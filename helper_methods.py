import requests
from requests.exceptions import SSLError
from bs4 import BeautifulSoup as soup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_soup_object_from_url(url):
    try:
        return soup(requests.get(url).content, 'html.parser')
    except SSLError:
        return soup(requests.get(url, verify=False).content, 'html.parser')


def convert_web_element_to_bs4_object(element):
    return soup(element.get_attribute('outerHTML'), 'html.parser')


def explicit_wait_css_selector(driver, delay, selector, single=True):
    if not single:
        return WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

    return WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )


def start_chrome_browser(driver_exe_file_path, url, headless=False):
    if headless:
        options = ChromeOptions()
        options.headless = True
        browser = Chrome(executable_path=driver_exe_file_path, options=options)
    else:
        browser = Chrome(executable_path=driver_exe_file_path)
    browser.get(url)
    return browser
