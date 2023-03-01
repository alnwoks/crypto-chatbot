import os
import requests

from bot_template import BOT_TEMPLATE


def send_telegram_message(chat_id, message):
    # Format the message using the bot template
    formatted_message = BOT_TEMPLATE.format(
        currency=message['currency'],
        exchange_name=message['exchange_name'],
        buy_rate=message['buy_rate'],
        sell_rate=message['sell_rate'],
        response_time=message['response_time']
    )

    # Send the formatted message back to the user via the Telegram bot
    telegram_bot_token = os.environ['telegram_bot_token']
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': formatted_message
    }
    response = requests.post(url, data=data)

    # Debugging feature: log the response to the console
    print(f"Telegram response: {response.text}")
