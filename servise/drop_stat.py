import os
import sys

import django
import telebot

sys.path.append('/home/apple/code/project1/tune/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tune.settings")
django.setup()
TOKEN = '5376806714:AAELQVr7_Xe648jHUnI6ZmVa32VPqikNz8Q'
client = telebot.TeleBot(TOKEN, threaded=False)
client.send_message(chat_id=572982939, text='ДРОП')
from tune_admin.models import StaticUserHourModel
# print(StaticUserHourModel.objects.filter().delete())
if __name__ == '__main__': pass
