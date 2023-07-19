from flask import Flask, request
from functions import *

# Define your bot token
# BOT_TOKEN = '6003301685:AAFSmqvk4IWe7mn9xt2HsLagLMjV1CIzpJA'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    update = request.get_json()

    # Initialize two variables used to respond to Telegram
    methods = []
    post_fields = [{}]

    # Do the thing
    echo_input(update)

    # Send it all to Telegram's servers using HTTP POST
    send_response(update)

    return 'OK'

if __name__ == '__main__':
    app.run()
