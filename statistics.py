import redis
from datetime import date, timedelta

#redis database 1 --> statistics database
r_stats = redis.StrictRedis(host='127.2.73.2', port=16379, db=1, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")

today = date.today()

#writes every chat_id into "unique_users" set - alltime and daily
def write_user_stats(chat_id):
    #unique users alltime
    r_stats.sadd("unique_users", chat_id)
    print "Unique users: "+ str(len(r_stats.smembers("unique_users")))

    #unique users today
    r_stats.sadd("unique_users:"+today, chat_id)
    print "Unique users today: "+ str(len(r_stats.smembers("unique_users:"+today)))

    #total requests
    r_stats.incr("requests_total")
    print "All requests: "+ str(r_stats.get("requests_total"))

    #dayli requests
    r_stats.incr("requests:"+today)
    print "All requests: "+ str(r_stats.get("requests"+today))


def write_sound_stats():
    stest = ""




def get_stats():
    unique_users = str(len(r_stats.smembers("unique_users")))
    return unique_users, "boob", "boobie"

