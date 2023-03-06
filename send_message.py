import os
import time
from selenium import webdriver
from telegram import Bot
# from telegram.ext import ParseMode
# from telegram.ext import Updater, CommandHandler

WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
WHATSAPP_USERS = os.environ.get('WHATSAPP_USERS').split(',')
SKIP_QR_CODE = os.environ.get('SKIP_QR_CODE', 'false').lower() == 'true'

# Initialize the Telegram bot using the API token stored in the environment variable
TELEGRAM_CHAT_IDS = os.environ.get('TELEGRAM_CHAT_IDS').split(',')
TELEGRAM_BOT_TOKEN = os.environ.get('YOUR_TELEGRAM_BOT_TOKEN', '')

# updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

def send_whatsapp_message(to_number, message):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(WHATSAPP_WEB_URL)

    if not SKIP_QR_CODE:
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
    bot = Bot(TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=chat_id, text=message) # parse_mode=ParseMode.MARKDOWN_V2

def send_messages(message):
    for user in WHATSAPP_USERS:
        send_whatsapp_message(user, message)

    for chat_id in TELEGRAM_CHAT_IDS:
        send_telegram_message(chat_id, message)
