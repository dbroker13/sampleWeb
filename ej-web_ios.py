from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.app.zip')
APPIUM = 'http://localhost:4723'

CAPS = {
    "deviceName": "iPhone 12 Pro Max",
    "udid": "00008101-001D45E41169001E",
    'platformName': 'iOS',
    "platformVersion": "16.3",
    'automationName': 'XCUITest',
    'browserName': 'Safari',
    "headspin:capture" : True
}

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
)
try:
    wait = WebDriverWait(driver, 10)
    driver.get('https://the-internet.herokuapp.com')
    form_auth_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Form Authentication')))
    form_auth_link.click()
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
    username.send_keys('tomsmith')
    password = driver.find_element(By.CSS_SELECTOR, '#password')
    password.send_keys('SuperSecretPassword!')
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout'))).click()
    wait.until(EC.url_to_be('https://the-internet.herokuapp.com/login'))

    flash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#flash')))
    assert 'logged out' in flash.text

finally:
    driver.quit()