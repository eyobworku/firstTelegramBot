import json
#import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
methods = []
post_fields = [{}]

print(str(BOT_TOKEN)+'   hi')

def echo_input(update):
        # Using the Telegram Bot API method "sendMessage",
        # https://core.telegram.org/bots/api#sendmessage
        methods.append('sendMessage')

        # It's going back to the same chat where it came from
        post_fields[0]['chat_id'] = update['message']['chat']['id']

        # The text being returned is just the whole object
        post_fields[0]['text'] = json.dumps(update,indent=2)

def send_response(update):
        # Now go through the array and send each method and post_fields
        for i in range(len(methods)):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/{methods[i]}"
            headers = {"Content-Type": "application/json"}
            #response = requests.post(url, headers=headers, json=post_fields[i])
            # Process the response if needed
