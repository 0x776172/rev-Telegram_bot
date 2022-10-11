from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import redis
import datetime as dt
import pytz

host = 'redis-17747.c302.asia-northeast1-1.gce.cloud.redislabs.com'
port = 17747
psw = 'AIg6dmxhPvYsTEc2vU8XNqWc96mSbv05'
r = redis.Redis(host=host, port=port, password=psw)
db_keys = r.keys(pattern='*')

updater = Updater(token='5758131204:AAHZB0J8JXGyuUTGV3IMzfMy4jx0pgjkcGs', use_context=True)
dp = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

job = updater.job_queue

def start(update, context):
  user_id = update.message.from_user.id
  user_name = update.message.from_user.name
  r.set(user_name, user_id)
  message = 'Bot Aktif'
  context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def stop(update, context):
  user_name = update.message.from_user.name
  r.delete(user_name)
  message = 'Bot Nonaktif'
  context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#task
j = updater.job_queue

# def once(context: CallbackContext):
#   msg = 'once'
#   for user in db_keys:
#     id = r.get(user).decode("UTF-8")
#     context.bot.send_message(chat_id=id, text=msg)

# j.run_once(once, 30)

def morning(context: CallbackContext):
  msg = 'Jangan Lupa Sarapan'
  for user in db_keys:
    id = r.get(user).decode('UTF-8')
    context.bot.send_message(chat_id=id, text=msg)

def noon(context: CallbackContext):
  msg = 'Udah Siang!!'
  msg2 = 'Makan!!'
  for user in db_keys:
    id = r.get(user).decode('UTF-8')
    context.bot.send_message(chat_id=id, text=msg)
    context.bot.send_message(chat_id=id, text=msg2)

def night(context: CallbackContext):
  msg = 'Makan Malemnya!!'
  for user in db_keys:
    id = r.get(user).decode('UTF-8')
    context.bot.send_message(chat_id=id, text=msg)

j.run_daily(morning,days=(range(7)), time=dt.time(hour=6, minute=00, tzinfo= pytz.timezone('Asia/Jakarta')))
j.run_daily(noon,days=(range(7)), time=dt.time(hour=13, minute=30, tzinfo= pytz.timezone('Asia/Jakarta')))
j.run_daily(night,days=(range(7)), time=dt.time(hour=19, minute=00, tzinfo= pytz.timezone('Asia/Jakarta')))
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
dp.add_handler(start_handler)
dp.add_handler(stop_handler)
updater.start_polling()