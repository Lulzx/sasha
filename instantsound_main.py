from flask import Flask, request
import telepot
import base64
from os import listdir, path
import time
from Queue import Queue
app = Flask(__name__)


#old function
# def handle(msg):
#     print msg
#     content_type, chat_type, chat_id = telepot.glance(msg)
#
#     #builds path to file
#     script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#     rel_path = "sounds/badumtss.mp4"
#     abs_file_path = os.path.join(script_dir, rel_path)
#
#     #opens file
#     music_file = open(abs_file_path, 'rb')
#
#     #sends it as voice message
#     bot.sendVoice(chat_id, music_file)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    msg_text = msg['text']
    print 'Chat Message:', msg

    if content_type != "text":
        pass

    # checks for /start command
    elif (msg_text.startswith("/get")) or (msg_text.startswith("/get@instantsoundbot")):
         #builds path to file
        script_dir = path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "sounds/badumtss.mp4"
        abs_file_path = path.join(script_dir, rel_path)

        #opens file
        music_file = open(abs_file_path, 'rb')

        #sends as file with title
        #bot.sendAudio(chat_id, music_file, title='badumtss')

        #gets message_id
        msg_id = msg['message_id']

        #sends it as voice message
        bot.sendVoice(chat_id, music_file, reply_to_message_id=msg_id)


    elif (msg_text[:5] == "/help") or (msg_text[:6] == "/start"):
        #sends /help and /Start message
        bot.sendMessage(chat_id,
                        "*Welcome to the instant sound bot*" + chr(10) +
                        "commands:" + chr(10) +
                        "/get [file_name].mp4 -> returns badumtss.mp4"+ chr(10) +
                        "/get keyword -> for search "+ chr(10) +
                        "/get -> sends random sound",
                        parse_mode="Markdown")




# def on_inline_query(msg):
#     query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
#     print 'Inline Query:', msg
#
#
#     # Compose your own answers
#     articles = [{'type': 'article',
#                     'id': '1', 'title': 'Badumtss', 'message_text': '/get@instantsoundbot badumtss'}]
#
#     bot.answerInlineQuery(query_id, articles)
#
#
#
# def on_chosen_inline_result(msg):
#     result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
#     print 'Chosen Inline Result:', result_id, from_id, query_string





TOKEN = base64.b64decode("MjA5Mjk0MDAyOkFBRjA4bUV4YWwxRVpfMHBUdXFSWFpVWnk0dmhTQWJTTUhZ")

#Flask routing and passing the POST to the queue test
app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.notifyOnMessage({'normal': on_chat_message}, source=update_queue) # take updates from queue



@app.route('/'+TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    app.run()