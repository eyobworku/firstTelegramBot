import json
import requests
import os
from db import insert_users,select_user,upate_user,delete_user,readJsonXl,create_and_insert_table,insert_reults,select_results,select_keys

BOT_TOKEN = '6003301685:AAFSmqvk4IWe7mn9xt2HsLagLMjV1CIzpJA'
# methods = []
# post_fields = [{}]


def echo_input(update):
        # Using the Telegram Bot API method "sendMessage",
        # https://core.telegram.org/bots/api#sendmessage
        # methods.append('sendMessage')

        # # It's going back to the same chat where it came from
        # post_fields[0]['chat_id'] = update['message']['chat']['id']
        if 'callback_query' in update and update['callback_query']:
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['callback_query']['message']['chat']['id']
            update['post_fields'][0]['text'] = json.dumps(update,indent=2)
        else:
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            update['post_fields'][0]['text'] = json.dumps(update,indent=2)

        # The text being returned is just the whole object
        # post_fields[0]['disable_web_page_preview'] = True

def send_response(update):
        # Now go through the array and send each method and post_fields
        for i in range(len(update['methods'])):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/{update['methods'][i]}"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=update['post_fields'][i])
            return response.json()
            # Process the response if needed

def route_requests(update):
    if 'callback_query' in update:
        if update['callback_query']['data']=='student' or update['callback_query']['data']=='instructor':
            perform_callback(update)
        else:
            deprt_callback(update)
        return

    if 'entities' in update['message'] and update['message']['entities'] and update['message']['entities'][0]['type'] == 'bot_command':
        update['parameters'] = []
        update['command'] = [update['message']['text'][0:update['message']['entities'][0]['length']]]
        update['parameters'].append(update['message']['text'][update['message']['entities'][0]['length']+1:])

        if update['command'][0] == '/whoami':
            # whoami(update)
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            update['post_fields'][0]['text'] ='who am i'
        elif update['command'][0] == '/echo':
            echo_input(update)
        elif update['command'][0] == '/start':
            view_menue(update)
        elif update['command'][0] == '/register':
            view_menue(update)
        elif str(update['command'][0]).startswith("/file_"):
            update['methods'] = ['sendMessage']
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            command = update['command'][0]
            myTable = command.split('/')[-1]
            result = select_keys(myTable,update['message']['chat']['id'])
            if len(result) > 0:
                update['post_fields'][0]['text'] = json.dumps(result,indent=2)
            else:
                update['post_fields'][0]['text'] = "Please login.\n/start"
        else:
            # bad_request(update)
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            update['post_fields'][0]['text'] ='bad request'
    elif 'document' in update['message'] and update['message']['document']:
        save_file(update)
    else:
        if 'reply_to_message' in update['message']:
            if update['message']['reply_to_message']['text']=='Enter your Id and Name.\n\ne.g 1372 Alazar':
                save_data(update)
        else:
            perform_text(update)

def save_file(update):
    chat_id = update['message']['chat']['id']
    myUser = select_user(chat_id)
    if 'chat_id' in myUser:
        myFile = {}
        myFile['methods'] = []
        myFile['post_fields'] = [{}]
        myFile['methods'].append('getFile')
        myFile['post_fields'][0]['file_id'] = update['message']['document']['file_id']
        myFile = send_response(myFile)

        url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{myFile['result']['file_path']}"
        response = requests.get(url)
        folder_path = 'savedFile'
        os.makedirs(folder_path, exist_ok=True)

        file_name = myFile['result']['file_path'].split('/')
        file_name = file_name[-1]
        my_file = os.path.join(folder_path,file_name)
        if response.status_code == 200:
            with open(my_file, 'wb') as file:
                file.write(response.content)
        fileName, keys, result = create_and_insert_table(my_file)
        if result:
            new = insert_reults(chat_id,fileName,keys)
            if new:
                text = 'You uploaded succesfully'
            else:
                text = 'You did not uploaded succesfully insertion'
        else:
            text = 'You did not uploaded succesfully'

        update['methods'].append('sendMessage')
        update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
        update['post_fields'][0]['text'] = text
    else:
        update['methods'].append('sendMessage')
        update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
        update['post_fields'][0]['text'] = 'Please login first.\n/start'

def view_menue(update):
    chat_id = update['message']['chat']['id']
    myUser = select_user(chat_id)
    if 'chat_id' in myUser:
        update['methods'].append('sendMessage')
        update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
        if myUser['roll'] == 'student':
            update['post_fields'][0]['text'] ='Welcome to our bot {}.'.format(myUser['name'])
            keyboard = [
            [{'text':'Show Posts'}],
            [{'text':'Delete Account'}]
        ]
            update['post_fields'][0]['reply_markup'] = json.dumps({
            'keyboard': keyboard,
            'resize_keyboard':True,
            'one_time_keyboard':True,
            'is_persistent':True,
            })
        else:
            update['post_fields'][0]['text'] ='Welcome to our bot Mr. {}.'.format(myUser['name'])
            keyboard = [
            [{'text':'Add new post'}],
            [{'text':'Delete Account'}]
        ]
            update['post_fields'][0]['reply_markup'] = json.dumps({
            'keyboard':keyboard,
            'resize_keyboard':True,
            'one_time_keyboard':True,
            'is_persistent':True,
            })
    else:
        update['methods'].append('sendMessage')
        update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
        update['post_fields'][0]['text'] ='Welcome to our bot.\nRegister as:'
        keyboard = [
        [{'text':'Student','callback_data':'student'}],
        [{'text':'Instructor','callback_data':'instructor'}]
    ]
        update['post_fields'][0]['reply_markup'] = json.dumps({
            'inline_keyboard':keyboard})

def perform_callback(update):
    if update['callback_query']['data']=='student':
        roll = 'student'
    else:
        roll = 'instructor'

    keyboard = [
    [{'text':'SE','callback_data':f'{roll}_SE'},{'text':'IT','callback_data':f'{roll}_IT'}],
    [{'text':'CS','callback_data':f'{roll}_CS'},{'text':'IS','callback_data':f'{roll}_IS'}]
    ]
    update['methods'].append('sendMessage')
    update['post_fields'][0]['chat_id'] = update['callback_query']['message']['chat']['id']

    update['post_fields'][0]['text'] = 'Choose your department!'#Enter your Id and Name.\n\ne.g 1372 Alazar
    update['post_fields'][0]['reply_markup'] = json.dumps({
        'inline_keyboard':keyboard,
        'force_reply':True
    })

    update['post_fields'].append({})
    update['methods'].append('answerCallbackQuery')
    update['post_fields'][1]['callback_query_id']=update['callback_query']['id']

def deprt_callback(update):
    values = update['callback_query']['data']
    value = values.split('_')
    chat_id = update['callback_query']['message']['chat']['id']
    result = insert_users(chat_id,value[0],value[1])
    if result:
        update['methods'].append('sendMessage')
        update['post_fields'][0]['chat_id'] = update['callback_query']['message']['chat']['id']

        update['post_fields'][0]['text'] = 'Enter your Id and Name.\n\ne.g 1372 Alazar'
        update['post_fields'][0]['reply_markup'] = json.dumps({
            'force_reply':True
            })

        update['post_fields'].append({})
        update['methods'].append('answerCallbackQuery')
        update['post_fields'][1]['callback_query_id']=update['callback_query']['id']

def save_data(update):
    chat_id = update['message']['chat']['id']
    myUser = select_user(chat_id)
    if 'chat_id' in myUser:
        values = update['message']['text'].split()
        result = upate_user(myUser['chat_id'],myUser['roll'],myUser['department'],values[0],values[1])
        if result==True:
            text = 'registered'
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            update['post_fields'][0]['text'] = text
            if myUser['roll'] == 'student':
                keyboard = [
                [{'text':'Show Posts'}],
                [{'text':'Delete Account'}]
            ]
                update['post_fields'][0]['reply_markup'] = json.dumps({
                'keyboard': keyboard,
                'resize_keyboard':True,
                'one_time_keyboard':True,
                'is_persistent':True,
                })
            else:
                keyboard = [
                [{'text':'Add new post'}],
                [{'text':'Delete Account'}]
            ]
                update['post_fields'][0]['reply_markup'] = json.dumps({
                'keyboard':keyboard,
                'resize_keyboard':True,
                'one_time_keyboard':True,
                'is_persistent':True,
                })
        else:
            text = 'not registered'
            update['methods'].append('sendMessage')
            update['post_fields'][0]['chat_id'] = update['message']['chat']['id']
            update['post_fields'][0]['text'] = text
    else:
        view_menue(update)

def perform_text(update):
    update['methods'].append('sendMessage')
    update['post_fields'][0]['chat_id'] = update['message']['chat']['id']

    text = update['message']['text']
    if text == 'Delete Account':
        result = delete_user(update['message']['chat']['id'])
        if result:
            update['post_fields'][0]['text'] = 'Deleted.'
        else:
            update['post_fields'][0]['text'] = 'Not deleted.'
    elif text == 'Add new post':
        update['post_fields'][0]['text'] = 'Please send me an excel file.\nWhich should contain an Id column and\nother information for students'
    elif text == 'Show Posts':
        chat_id = update['message']['chat']['id']
        result = select_results(chat_id)
        if len(result) > 0:
            text = 'Posts for you:\n\n{}'.format("\n".join(["/{}".format(item[0]) for item in result]))
        else:
            text = 'There is no items for you.'
        update['post_fields'][0]['text'] = text
    else:
        update['post_fields'][0]['text'] = "I didn't understand that."