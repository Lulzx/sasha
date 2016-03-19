from flask import Flask, request
import telepot
import base64
import random
from os import listdir, path
from Queue import Queue
app = Flask(__name__)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    msg_text = msg['text']
    print 'Chat Message:', msg

    if content_type != "text":
        pass

    # checks for /start command
    elif msg_text.startswith("/get"):
        # absolute dir the script is in
        script_dir = path.dirname(__file__)

        #builds path to file
        rel_path = "sounds/badumtss.mp4"
        abs_file_path = path.join(script_dir, rel_path)

        #file_list from directory sounds/
        sounds_dir = path.join(script_dir, "sounds")
        file_list = listdir(sounds_dir)
        print sounds_dir
        print file_list

        #opens file
        music_file = open(abs_file_path, 'rb')

        #sends as file with title
        #bot.sendAudio(chat_id, music_file, title='badumtss')

        #gets message_id
        msg_id = msg['message_id']

        #sends it as voice message
        bot.sendChatAction(chat_id, "upload_audio")
        bot.sendVoice(chat_id, music_file, reply_to_message_id=msg_id)


    ### /random command ###
    #sends random soundfile from /sounds
    elif msg_text.startswith("/random"):
        # absolute dir the script is in
        script_dir = path.dirname(__file__)

        #file_list from directory /sounds
        sounds_dir = path.join(script_dir, "sounds")
        file_list = listdir(sounds_dir)

        #gets random number out length from file_list
        rnd_num_filelist = random.randrange(0,len(file_list))
        rnd_file= file_list[rnd_num_filelist]

        #builds path to file
        abs_file_path = path.join(script_dir, "sounds/"+rnd_file)

        #opens file
        music_file = open(abs_file_path, 'rb')

        #gets message_id
        msg_id = msg['message_id']

        #sends it as voice message
        bot.sendChatAction(chat_id, "typing")
        bot.sendMessage(chat_id,  rnd_file)
        bot.sendChatAction(chat_id, "upload_audio")
        bot.sendVoice(chat_id, music_file)


    ### /help command ###
    #sends /help and /Start message
    elif (msg_text[:5] == "/help") or (msg_text[:6] == "/start"):

        bot.sendMessage(chat_id,
                        "*Welcome to the Instant Sound Bot*\n"
                        "*Use the following commands:*\n"
                        "\n"
                        "`/get [file_name].mp4`\n"
                        "--> eg. '`/get badumtss.mp4`'\n"
                        "\n"
                        "`/search [keyword]` \n"
                        "--> search for a sound\n"
                        "\n"
                        "`/random`\n"
                        "--> sends random sound\n "
                        "\n"
                        "`/list A` \n"
                        "--> lists all sounds who start with a",
                        parse_mode="Markdown")


    ### /list command ###
    #lists all sounds who start with x
    elif (msg_text[:5] == "/list"):
        #gets the key letter "/list [key]"
        key_letter = msg_text[6:8].lower()
        print key_letter

        #checks if keyletter is specified
        if key_letter:
            # absolute dir the script is in
            script_dir = path.dirname(__file__)

            #file_list from directory /sounds
            sounds_dir = path.join(script_dir, "sounds")
            file_list = listdir(sounds_dir)

            #creates a list of all filenames who start with x
            string_x = ""
            for i in file_list:
                if i.startswith(key_letter):
                    string_x = string_x + i + "\n"

            #if no file is found
            if not string_x:
                string_x = "No sound with "+key_letter+" found"


            bot.sendMessage(chat_id, string_x, parse_mode="HTML")
        else:
            bot.sendMessage(chat_id, "You need to specify a character\ne.g. '/list A'", parse_mode="Markdown")





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