import redis
from datetime import date, timedelta

#redis database 1 --> statistics database
r_stats = redis.StrictRedis(host='127.2.73.2', port=16379, db=1, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")

#writes every chat_id into "unique_users" set
def write_user_stats(chat_id):
    r_stats.sadd("unique_users", chat_id)
    print "Unique users:"+ len(r_stats.smembers())

def write_daily_stats():
    today = date.today()
    test = ""



def get_stats():
    return "bob", "boob", "boobie"

