import os
import logging
import time
from selenium import webdriver
from telegram import Bot
# from telegram.ext import ParseMode
# from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
WHATSAPP_USERS = os.environ.get('WHATSAPP_USERS').split(',')
SKIP_QR_CODE = os.environ.get('SKIP_QR_CODE', 'false').lower() == 'true'

# Initialize the Telegram bot using the API token stored in the environment variable
TELEGRAM_CHAT_IDS = os.environ.get('TELEGRAM_CHAT_IDS').split(',')
TELEGRAM_BOT_TOKEN = os.environ.get('YOUR_TELEGRAM_BOT_TOKEN', '')

# updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

def send_whatsapp_message(to_number, message):
    try:
        # Set up the Chrome driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Open the WhatsApp Web page and wait for it to load
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(WHATSAPP_WEB_URL)
        time.sleep(10)

        if not SKIP_QR_CODE:
            input('Press enter after scanning QR code')

        search_box = driver.find_element("xpath",'//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(to_number)
        time.sleep(5)

        # Find the user's chat box and click on it
        user_box = driver.find_element("xpath",f'//span[@title="{to_number}"]')
        user_box.click()
        time.sleep(5)

        # Find the message input box and send the message
        message_box = driver.find_element("xpath", '//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')
        message_box.click()
        message_box.send_keys(message)
        time.sleep(5)

        # Find the send button and click on it
        send_button = driver.find_element("xpath",'//span[@data-icon="send"]')
        send_button.click()
        time.sleep(5)
        
        # Close the Chrome driver
        driver.quit()
    except Exception as e:
        logger.error(f'Error sending WhatsApp message: {e}')


def send_telegram_message(chat_id, message):
    try:
        bot = Bot(TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=chat_id, text=message) # parse_mode=ParseMode.MARKDOWN_V2
    except Exception as e:
        logger.error(f'Error sending Telegram message: {e}')
    
def send_messages(message):
    for user in WHATSAPP_USERS:
        send_whatsapp_message(user, message)

    for chat_id in TELEGRAM_CHAT_IDS:
        send_telegram_message(chat_id, message)
