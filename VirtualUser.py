from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import json
from selenium.webdriver.support import expected_conditions as EC
from Field import Field


class VirtualUser:
    """ Class that handles user interaction on each page specific structure"""

    def __init__(self, driver):
        self.driver = driver
        self.originalWindow = self.driver.current_window_handle
        self.wait = WebDriverWait(self.driver, 10)
        assert len(self.driver.window_handles) == 1

    def do_gmail_login(self):
        """ Login via gmail and switch handles so you can interact with the 
            original window. It's fine to have everything cluttered here
            as this is just a setup."""
        self._close_cookies()
        usernameValue = self._get_credential_field('username')
        passwordValue = self._get_credential_field('password')
        gmailBtn = self._get_element(
            {'by': By.CSS_SELECTOR, 'value': '.google'})
        gmailBtn.click()

        self.wait.until(EC.number_of_windows_to_be(2))

        self.switch_to_current_window()

        usernameElement = self._get_loading_element(
            {'by': By.CSS_SELECTOR, 'value': 'input[type="email"]'})

        usernameField = Field(usernameElement)

        usernameField.populate_field_and_send(usernameValue)

        passwordElement = self._get_loading_element(
            {'by': By.CSS_SELECTOR, 'value': 'input[type="password"].whsOnd'})

        passwordField = Field(passwordElement)
        passwordField.populate_field_and_send(passwordValue)

        self.switch_to_window(self.originalWindow)

    def do_login(self):
        pass

    def _close_cookies(self):
        cookieBtn = self.wait.until(EC.element_to_be_clickable(
            (By.ID, 'onetrust-accept-btn-handler')))
        cookieBtn.click()

    def _get_loading_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(
            (locator['by'], locator['value'])))
        return element

    def _get_element(self, locator):
        element = self.driver.find_element(locator['by'], locator['value'])
        return element

    def _get_credential_field(self, field):
        ' Gets the credential fields to do the login '
        with open("credentials.json", 'r') as credentials:
            data = credentials.read()
        credentialsParsed = json.loads(data)
        return credentialsParsed[0][field]

    def perform_search(self, keywordsField, locationField, actionEl):
        keywordsField.populate_field('front end', self.driver)
        locationField.populate_field('edgware london', self.driver)
        actionEl.click()

    def set_action_fields(self, inputKeywords, inputLocation, actionBtn):
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-1etjok6')))
        self.interactHandler(
            {'by': By.ID, 'value': 'onetrust-accept-btn-handler'})
        self.inputKeywords = self.find_element(
            {'by': By.ID, 'value': 'sc.keyword'})
        self.inputLocation = self.find_element(
            {'by': By.ID, 'value': 'sc.location'})
        self.actionBtn = self.find_element(
            {'by': By.CSS_SELECTOR, 'value': '[data-test = "search-bar-submit"]'})

    def close_interactable_element(self, element):
        element.click()

    def click_interact(self, element):
        element.click()

    def switch_to_window(self, window):
        self.driver.switch_to.window(window)

    def switch_to_current_window(self):
        for window_handle in self.driver.window_handles:
            if window_handle != self.originalWindow:
                self.driver.switch_to.window(window_handle)
                break
