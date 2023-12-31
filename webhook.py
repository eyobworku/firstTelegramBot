from flask import Flask, request
from functions import *
# from bson.objectid import ObjectId
# import os

# Define your bot token
app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    update = request.get_json()

    # Initialize two variables used to respond to Telegram
    update['methods'] = []
    update['post_fields'] = [{}]

    # Do the thing
    route_requests(update)
    # echo_input(update)

    # Send it all to Telegram's servers using HTTP POST
    send_response(update)

    return 'OK'

@app.route('/', methods=['GET'])
def index():
    return '<h1>Added user</h1>'


# if __name__ == '__main__':
#     app.run()
