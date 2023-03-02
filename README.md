### crypto-chatbot
## Testing the Telegram and WhatsApp Handlers Locally

To test the Telegram and WhatsApp handlers locally, follow these steps:

1. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```
2. Install the required serverless plugins:

   ```sh
   serverless plugin install -n serverless-python-requirements
   serverless plugin install -n serverless-offline
   serverless plugin install -n serverless-dotenv-plugin
   ```
3. Start the local serverless server:

   ```sh
   sls offline start
   ```
4. In a separate terminal window, invoke the Telegram handler with a test event:

   ```sh
   serverless invoke local --function telegram --data '{"message": {"text": "/crypto"}}'

   ```
   Note that when invoking the Telegram function, you must pass a JSON object with a `message` property that contains the `text` of the message that you want to send to the bot. In this example, we are sending the `/crypto` command to trigger the function.

5. In another separate terminal window, invoke the WhatsApp handler with a test event:

   ```sh
   serverless invoke local --function whatsapp

   ```
   When invoking the WhatsApp function, no input data is needed, since the function simply sends the latest crypto rates to the user via WhatsApp.

6. Check the response messages printed to your console.

Note that you'll need to add/update the values in the `.env` file with your own bot tokens.



