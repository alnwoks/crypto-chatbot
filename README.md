### crypto-chatbot
## Testing the Telegram and WhatsApp Handlers Locally

To test the Telegram and WhatsApp handlers locally, follow these steps:

1. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```
2. Start the local serverless server:

   ```sh
   sls offline start
   ```
3. In a separate terminal window, invoke the Telegram handler with a test event:

   ```sh
   sls invoke local -f telegram_handler --data '{"message": {"chat": {"id": "test_chat_id"}, "text": "btc"}}'
   ```
   Replace `test_chat_id` with your own Telegram chat ID, and replace `btc` with the cryptocurrency you want to get rates for.
   This sends a test message for BTC rates to the Telegram bot running on your local server.

4. In another separate terminal window, invoke the WhatsApp handler with a test event:

   ```sh
   sls invoke local -f whatsapp_handler --data '{"From": "test_chat_id", "Body": "eth"}'
   ```
   Replace `test_chat_id` with your own WhatsApp chat ID, and replace `eth` with the cryptocurrency you want to get rates for.
   This sends a test message for ETH rates to the WhatsApp bot running on your local server.

5. Check the response messages printed to your console.

Note that you'll need to update the `YOUR_TELEGRAM_BOT_TOKEN` and `YOUR_WHATSAPP_BOT_TOKEN` values in the `serverless.yml` file with your own bot tokens.



