from flask import Flask, request
# from functions import *
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
import os

# Define your bot token
# BOT_TOKEN = '6003301685:AAFSmqvk4IWe7mn9xt2HsLagLMjV1CIzpJA'

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://eyob:12345ewp@mydatabase.g895nzq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo()
mongo.init_app(app)

# @app.route('/', methods=['POST'])
# def webhook():
#     # Get the JSON data from the request
#     update = request.get_json()

#     # Initialize two variables used to respond to Telegram
#     methods = []
#     post_fields = [{}]

#     # Do the thing
#     echo_input(update)

#     # Send it all to Telegram's servers using HTTP POST
#     send_response(update)

#     return 'OK'

@app.route('/', methods=['GET'])
def index():
    db = mongo.db
    bool = db.user.insert_one({'name':'test'})
    if(bool.acknowledged):
        return '<h1>Added user</h1>'
    else:
        return '<h1>Not added user</h1>'

# if __name__ == '__main__':
#     app.run()
