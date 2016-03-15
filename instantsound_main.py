from flask import Flask, request
import telepot
import base64
import os
from Queue import Queue
app = Flask(__name__)

def handle(msg):
    print msg
    content_type, chat_type, chat_id = telepot.glance(msg)

    #builds path to file
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "sounds/badumtss.mp4"
    abs_file_path = os.path.join(script_dir, rel_path)

    #opens file
    music_file = open(abs_file_path, 'rb')

    #sends it as voice message
    bot.sendVoice(chat_id, music_file)




TOKEN = base64.b64decode("MjA5Mjk0MDAyOkFBRjA4bUV4YWwxRVpfMHBUdXFSWFpVWnk0dmhTQWJTTUhZ")

#Flask routing and passing the POST to the queue test
app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.notifyOnMessage(handle, source=update_queue)  # take updates from queue

@app.route('/'+TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    app.run()