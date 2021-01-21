from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class Field:
    def __init__(self, element):
        self.field = element

    def populate_field(self, value, driver):  #
        if self._has_input_value(self.field):
            self._clear_field(driver)
        self.field.send_keys(value)

    def _has_input_value(self, el):
        """Check if the input element has a value already"""
        val = el.get_attribute('value')
        return True if val else False

    def _clear_field(self, driver):
        self.field.send_keys('')
        actionClear = ActionChains(driver)
        actionClear.key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).perform()

    def populate_field_and_send(self, value):
        self.field.send_keys(value + Keys.ENTER)
