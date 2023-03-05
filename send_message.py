import os
import time
from selenium import webdriver

WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'

def send_whatsapp_message(to_number, message):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(WHATSAPP_WEB_URL)

    input('Press enter after scanning QR code')
    
    search_box = driver.find_element_by_xpath('//div[contains(@class, "_2_1wd copyable-text selectable-text")]')
    search_box.click()
    search_box.send_keys(to_number)

    user_box = driver.find_element_by_xpath(f'//span[@title="{to_number}"]')
    user_box.click()

    message_box = driver.find_element_by_xpath('//div[contains(@class, "_2_1wd copyable-text selectable-text")]')
    message_box.click()
    message_box.send_keys(message)

    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')
    send_button.click()

    driver.quit()

def send_telegram_message(chat_id, message):
    pass
