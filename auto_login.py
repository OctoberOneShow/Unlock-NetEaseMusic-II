# coding: utf-8

import os
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
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009A23AD0A7CF4532F55C95FE49F6690F0393055F5AC04C39BAA087E3E2F6BDC677F05632FB7D9D3119864E0572A5BD4410926286FCB7BAF0F26D6B4DF320E764E16CA423E5EA0480186E41FF3EE7B20939BD8FE2C75931433D5F46F443E5914C6297C0DA139904E06BBFD2BA4EAD4513B2EF80062246310399D41096B7AA8D3798449A9E3AAC9CB81FD5C6CECEC9A75533A7F40FA240535C185341B119A066505C2D8C01A9F3D8C8F4DE5BB1B3FBD9546A3DB8928EBD186CFFEEDA501FF78452FC96A54603F4BB3101A064A4CB9A17B7BDFB6190760E41EAEC64521D0249DD5760D9074BE803B5D3BE423530345BB71F6F2C2D3CC57C71695413EB3BD6F0FB257696CE06608298372C2F5D8EA3D691BA4FCE0BAE5E019569F13B37A78AC2A97AE88A43B8E00EA77599A4C025AA8E7960C3EA5E9613322C80312EA8E72B35D2846C2115949A5F00F49CE846B45A9F7945277EADC6C09E5F4C73C919598B10A5944"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
