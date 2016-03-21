import redis
from os import listdir, path


def setFilelist():
    r = redis.StrictRedis(host='127.2.73.2', port=16379, db=0, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")

    # absolute dir the script is in
    script_dir = path.dirname(__file__)

    #file_list from directory sounds/
    sounds_dir = path.join(script_dir, "sounds")
    file_list = listdir(sounds_dir)

    #write to redis datastore sound:[filename].mp4 -> filename
    for i in file_list:
        r.set("sound:"+str(i), i[:-4])
        print r.get('sound:'+str(i))
