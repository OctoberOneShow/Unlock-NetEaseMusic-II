# coding: utf-8

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]"))
        )
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        # ✅ 使用 win64 架构的 chromedriver
        service = Service(ChromeDriverManager(os_type="win64").install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    browser.implicitly_wait(20)
    browser.get('https://music.163.com')

    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({
        "name": "MUSIC_U",
        "value": "00CFF165C9F8EF1054F4A1C01327891C487F39FDC5A2E3D806DE88558D3036639A2E229C8A7E464EFF734A4B00D6B3F61CCB7E30943B142308462F41B69A2E6C5BFF870796197500DF1BC3E2E6C2979ABCE665AC6FFE37C6AA2F8AD90CA29141271E3A41FF59FF134963F181BC18199BDD19F0492B804B41421DD85C405C77961E5695A479DCE53C76232EC932D0C00F4B69F5A7C1C18B62981B0C9145A142233C7314F77FAAF20310F49C96E315FA9F3067B52E9B9153197F034E724D2EDB24C8A0C1770C18D74D43B764CBCCE4D5ACE1E7D1F004B6D7EF9A7ADE5FA9E8412D22054D79C9C03AD0AE9635C00EA636D73790FC4CA369793D4DF2B975CD392A76683E3B4F3E174808DDCFF9185DD4D0D307166A9F149801138A347C5A0B268E89757DBFAC89A42F72316065C1B76B300FAB4F2AFDB6558B7338535DABD7F3A5921D8CC712499B8752F69323EA1360ACAC768B35E6B0F705FB2695FFEBBDDA38CADB"
    })

    browser.refresh()
    time.sleep(5)
    logging.info("Cookie login successful")

    logging.info("Unlock finished")
    time.sleep(10)
    browser.quit()

if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
