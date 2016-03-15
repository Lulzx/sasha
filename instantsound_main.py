from flask import Flask, request
import telepot
import base64
import os
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
    print 'Chat Message:', msg

     #builds path to file
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "sounds/badumtss.mp4"
    abs_file_path = os.path.join(script_dir, rel_path)

    #opens file
    music_file = open(abs_file_path, 'rb')

    #sends it as voice message
    bot.sendVoice(chat_id, music_file)

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print 'Inline Query:', query_id, from_id, query_string

    #builds path to file
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "sounds/badumtss.mp4"
    abs_file_path = os.path.join(script_dir, rel_path)

    #opens file
    music_file = open(abs_file_path, 'rb')


    # Compose your own answers
    articles = [{'type': 'video',
                    'id': '1', 'title': 'badumtss', 'thumb_url': 'http://www.myinstants.com/media/images/transparent_button_small_normal.png', 'video_url': 'http://www.myinstants.com/media/sounds/trollolol.swf.mp3', 'mime_type': 'video/mp4', 'message_text': 'Badumtss'}]

    bot.answerInlineQuery(query_id, articles)



def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print 'Chosen Inline Result:', result_id, from_id, query_string

    #builds path to file
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "sounds/badumtss.mp4"
    abs_file_path = os.path.join(script_dir, rel_path)

    #opens file
    music_file = open(abs_file_path, 'rb')

    #sends it as voice message
    bot.sendVoice(from_id, music_file)




TOKEN = base64.b64decode("MjA5Mjk0MDAyOkFBRjA4bUV4YWwxRVpfMHBUdXFSWFpVWnk0dmhTQWJTTUhZ")

#Flask routing and passing the POST to the queue test
app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.notifyOnMessage({'normal': on_chat_message,
                     'inline_query': on_inline_query,
                     'chosen_inline_result': on_chosen_inline_result}, source=update_queue) # take updates from queue



@app.route('/'+TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    app.run()