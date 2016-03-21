import redis
from os import listdir, path

r = redis.StrictRedis(host='127.2.73.2', port=16379, db=0, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")

# absolute dir the script is in
script_dir = path.dirname(__file__)
#file_list from directory sounds/
sounds_dir = path.join(script_dir, "sounds")
file_list = listdir(sounds_dir)

#creates a file list in redis -  sound:[filename].mp4 -> filename
def setFilelist():
    #write to redis datastore sound:[filename].mp4 -> filename
    r.flushdb()
    print "DB FLUSHED"


#creates a set with all filenames
def createFile_Set():
    #adds all files from folder /sounds
    for i in file_list:
        r.sadd("file_list", i)
    print r.smembers("file_list")


#creates a set with filenames for all files who start with X
def createFile_Setx():
    for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
        files_with_x = [f for f in listdir(sounds_dir) if f[0] == i]
        for j in files_with_x:
            r.sadd("sounds:"+i, j)

        print r.smembers("sounds:"+i)
