from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from Page import Page
import time

options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.headless = False
options.page_load_strategy = 'eager'

# options.add_argument('--headless')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

driverGlassdoor = webdriver.Chrome(
    executable_path=r'C:\chromedriver.exe', options=options)


glassdoorPage = Page(driver=driverGlassdoor,
                     link="https://www.glassdoor.co.uk/index.htm")
glassdoorPage.run()
