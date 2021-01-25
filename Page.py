from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from JobElement import JobElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from UseDatabase import UseDatabase
from VirtualUser import VirtualUser
from Field import Field
from HTMLExtractor import HTMLExtractor
import copy
import asyncio
import json
import time

dbconfig = {
    'user': 'root',
    'password': '3dLIaPIdB3n3d1c',
    'host': '127.0.0.1',
    'database': 'jobs_search'
}


class Page:
    """ Class that handles parsing and result processsing actions"""

    def __init__(self, driver, link):
        self.driver = driver
        self.virtualUser = VirtualUser(self.driver)
        self.done = False
        self.driver.maximize_window()
        self.driver.get(link)
        self.run()

    def run(self):
        self._do_setup()
        while self.done != True:
            self.navigate_to_searchable_state()
            
    def navigate_to_searchable_state(self):
        self.perform_search()

        jobs_list = self.driver.find_elements_by_xpath('//ul[contains(@class, "jlGrid")]/li')

        once = True

        for job in jobs_list:
            link = job.find_element_by_xpath('.//div/a')
            link.click()
            if once:
                self.do_once()
                once = False
            self.extractHTML()

    def do_once(self):
        try:
            overlay = self.virtualUser.wait.until(lambda d: d.find_element_by_css_selector('.modal_closeIcon'))
            overlay.click()
        except:
            print('overlay should be closed f')

    def _do_setup(self):
        self.virtualUser.do_gmail_login()

    def _get_loading_element(self, locator):
        element = self.virtualUser.wait.until(EC.element_to_be_clickable(
            (locator['by'], locator['value'])))
        return element

    def perform_search(self):
        keywordsElement = self._get_loading_element(
            {'by': By.ID, 'value': 'sc.keyword'})
        locationElement = self._get_loading_element(
            {'by': By.ID, 'value': 'sc.location'})
        self.keywordsField = Field(keywordsElement)
        self.locationField = Field(locationElement)
        self.actionBtn = self._get_loading_element(
            {'by': By.CSS_SELECTOR, 'value': '.SearchStyles__newSearchButton'})
        self.virtualUser.perform_search(
            self.keywordsField, self.locationField, self.actionBtn)

    def _get_element(self, selector):
        el = self.driver.find_element(selector['by'], selector['value'])
        return el

    def interact_handler(self, selector):
        try:
            el = self.driver.find_element(selector['by'], selector['value'])
            self.handleElementInteraction(el)
        except ElementNotInteractableException:
            print('Element not interactable or doesn\'t exist')
        except NoSuchElementException:
            print('No such element exception')

    def handleElementInteraction(self, element):
        element.click()

    def extractHTML(self):
        self.virtualUser.wait.until(EC.presence_of_element_located((By.ID, "JDWrapper")))
        self.virtualUser.wait.until(EC.presence_of_element_located((By.ID, "HeroHeaderModule")))
        page_source = self.driver.page_source
        extractor = HTMLExtractor(page_source)
        fields = extractor.extract()
        print(fields)


    def save_to_database(self, JobsData):
        for job in JobsData:
            with UseDatabase(dbconfig) as cursor:
                _SQL = """INSERT INTO job_list 
                        (company_name, job_title, location, posted_on, infoHTML, apply_link) 
                        VALUES(%s, %s, %s, %s, %s, %s)"""
                val = (job.company_name, job.job_title,
                       job.location, job.posted_on, job.infoHTML, job.apply_link)
                cursor.execute(_SQL, val)
