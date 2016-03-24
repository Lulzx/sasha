import redis
from datetime import date, timedelta

#redis database 1 --> statistics database
r_stats = redis.StrictRedis(host='127.2.73.2', port=16379, db=1, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")

#redis database 0 for fileset
r = redis.StrictRedis(host='127.2.73.2', port=16379, db=0, password="ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5")


#writes every chat_id into "unique_users" set - alltime and daily
def write_user_stats(chat_id):

    date_today = date.today()
    today = date_today.strftime('%d/%m/%Y')

    #unique users alltime
    r_stats.sadd("unique_users", chat_id)
    print "Unique users: "+ str(len(r_stats.smembers("unique_users")))

    #unique users today
    r_stats.sadd("unique_users:"+today, chat_id)
    print "Unique users today: "+ str(len(r_stats.smembers("unique_users:"+today)))

    #total requests
    r_stats.incr("requests_total")
    print "Requests total: "+ str(r_stats.get("requests_total"))

    #dayli requests
    r_stats.incr("requests:"+today)
    print "Requests today: "+ str(r_stats.get("requests:"+today))


#writes all sounds send to the datastore
def write_sound_stats(file_name):
    #increments for every sound sent
    r_stats.incr("sounds_sent")
    print r_stats.get("sounds_sent")

    #sets "file_name.mp4" -> +1, useful to see which sound is requested the most
    r_stats.incr(file_name)
    print r_stats.get(file_name)


# generator function used to iterate over date range
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



def get_stats():
    date_today = date.today()
    today = date_today.strftime('%d/%m/%Y')

    #writes all stats in a dictionary and returns the dict
    stats = {'stats_date': today,
             'unique_users': len(r_stats.smembers("unique_users")),
             'unique_users_today': len(r_stats.smembers("unique_users:"+today)),
             'requests_total': r_stats.get("requests_total"),
             'requests_today':r_stats.get("requests:"+today),
             'sounds_sent': r_stats.get("sounds_sent")}


    #iterates from startdate to enddate
    start_date = date(2016, 03, 23)
    end_date = date_today
    date_list = []
    daily_requests = []
    for single_date in daterange(start_date, end_date):
        date_list.append(single_date.strftime('%d/%m/%Y'))
        daily_requests.append(r_stats.get("requests:"+single_date.strftime('%d/%m/%Y')))

    return (stats, date_list, daily_requests)



def get_sound_stats():
    #gets the file_list from redis set
    file_set = list(r.smembers("file_list"))

    #makes a dict with filename and usage stat {filename.mp4: 12}
    sound_stats = {}
    for i in file_set:
        if r_stats.get(i):
            sound_stats[i] = r_stats.get(i)

    return sound_stats
