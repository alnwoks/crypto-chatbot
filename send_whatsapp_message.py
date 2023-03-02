import os
import requests

from bot_template import BOT_TEMPLATE


def send_whatsapp_message(chat_id, message):
    # Format the message using the bot template
    formatted_message = BOT_TEMPLATE.format(
        currency=message['currency'],
        exchange_name=message['exchange_name'],
        buy_rate=message['buy_rate'],
        sell_rate=message['sell_rate'],
        response_time=message['response_time']
    )

    # Send the formatted message back to the user via the WhatsApp bot
    whatsapp_bot_token = os.environ['whatsapp_bot_token']
    url = f"https://api.chat-api.com/instance/{whatsapp_bot_token}/sendMessage"
    data = {
        'phone': chat_id,
        'body': formatted_message
    }
    response = requests.post(url, json=data)

    # Debugging feature: log the response to the console
    print(f"WhatsApp response: {response.text}")
