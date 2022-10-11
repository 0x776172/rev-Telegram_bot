import redis

host = 'redis-17747.c302.asia-northeast1-1.gce.cloud.redislabs.com'
port = 17747
psw = 'AIg6dmxhPvYsTEc2vU8XNqWc96mSbv05'
r = redis.Redis(host=host, port=port, password=psw)
db_keys = r.keys(pattern='*')

print(len(db_keys))

for single in db_keys:
  chat_id = r.get(single).decode("UTF-8")
  print(single.decode("UTF-8"), ": ", chat_id)