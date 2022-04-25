# import telebot


# # TELEGRAM_URL = 'https://api.telegram.org/bot5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
# TOKEN = '5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
# URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/cde3fe41e972cc1f1501bbd0a6d330a11644378495/'
# client = telebot.TeleBot(TOKEN)
# client.delete_webhook()
# # client.set_webhook(url='https://tuneapple.pythonanywhere.com/api')

# menu_support = ['-📱 iPhone', '-📲 iPad', '-💻 MacBook',
#                 '-🎧 AirPods', '-⌚ Watch',
#                 '-⌨ Устройства', '⬅️Главное меню']

# sup_callback = ['Назад к б\у iPhone', 'Назад к б\у  iPad', 'Назад к б\у MacBook',
#                 'Назад к б\у AirPods', 'Назад к б\у Watch',
#                 'Назад к б\у Устройства']

import io
import requests
from PIL import Image

username = 'TuneApple'
token = 'd1cfd6bbfc894c3592932df061dd238d291fb5e3'
domain_name = 'TuneApple.pythonanywhere.com'

def restart_server():
    response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}'.format(
            username=username,
            path='/home/TuneApple/tune/media'
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    return response.json()

result = restart_server()

keys = [i for i in result]
links_image = []
for link in keys:
    s = result[link]['url']
    links_image.append(s)

for i in links_image:
    response = requests.get(
        i,
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    con = response.content
    image = Image.open(io.BytesIO(con))
    # image = Image.frombytes('RGBA', (128,128), con)
    name = i.split('/')[-1]
    image.save("/home/apple/code/project1/tune/media/" + name)
    print(name)
