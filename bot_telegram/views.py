# import time

# import MySQLdb
# import telebot
# import requests
# from django.views.decorators.csrf import csrf_exempt
# from django.core.exceptions import PermissionDenied
# from django.http import HttpResponse
# TOKEN = '5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
# URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/da97163b8abb1a6488ea319e345377da1645036172/'
# client = telebot.TeleBot(TOKEN, threaded=False)
# # client.delete_webhook()



# menu_support = ['📱 iPhone', '📲 iPad', '💻 MacBook',
#                 '🎧 AirPods', '⌚ Watch',
#                 '⌨ Устройства', '⬅️Главное меню']

# sup_callback = ['Назад к Б/У iPhone', 'Назад к Б/У iPad', 'Назад к Б/У MacBook',
#                 'Назад к Б/У AirPods', 'Назад к Б/У Watch',
#                 'Назад к Б/У Устройства']

# connect = MySQLdb.connect('TuneApple.mysql.pythonanywhere-services.com', 'TuneApple', 'I1QEvAR503', 'TuneApple$TuneProd')

# cursor = connect.cursor()
# @csrf_exempt
# def bot(request):

#     if request.META['CONTENT_TYPE'] == 'application/json':
#         try:

#             json_data = request.body.decode('utf-8')
#             update = telebot.types.Update.de_json(json_data)
#             client.process_new_updates([update])
#             print('-----------------------4')
#             return HttpResponse({'200': 'ok'})

#         except:

#             json_data = request.body.decode('utf-8')
#             update = telebot.types.Update.de_json(json_data)
#             client.process_new_updates([update])
#             print('+++++++++++++++++++++++4')
#             return HttpResponse({'200': 'ok'})

#     else:
#         raise PermissionDenied


# def get_category():
#     cursor = connect.cursor()
#     sql = "SELECT * FROM TuneApple$TuneProd.tune_admin_category"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_category', result)
#     cursor.close()
#     return result


# def get_products(category_name):
#     cursor = connect.cursor()
#     sql = f"SELECT TuneApple$TuneProd.tune_admin_seriescategory.id, TuneApple$TuneProd.tune_admin_product.name" \
#           f" FROM TuneApple$TuneProd.tune_admin_seriescategory, TuneApple$TuneProd.tune_admin_product" \
#           f" WHERE TuneApple$TuneProd.tune_admin_seriescategory.category = '{category_name}'" \
#           f" AND TuneApple$TuneProd.tune_admin_product.series_id = TuneApple$TuneProd.tune_admin_seriescategory.id" \
#           f" AND sell != 1"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_products')
#     cursor.close()
#     return result


# def get_products_a(category_name):
#     cursor = connect.cursor()
#     sql = f"SELECT TuneApple$TuneProd.tune_admin_seriescategory.id, TuneApple$TuneProd.tune_admin_product.name" \
#           f" FROM TuneApple$TuneProd.tune_admin_seriescategory, TuneApple$TuneProd.tune_admin_product" \
#           f" WHERE TuneApple$TuneProd.tune_admin_seriescategory.category LIKE '%{category_name}%'" \
#           f" AND TuneApple$TuneProd.tune_admin_product.series_id = TuneApple$TuneProd.tune_admin_seriescategory.id" \
#           f" AND sell != 1"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_products_a')
#     cursor.close()
#     return result


# def get_current_product():
#     cursor = connect.cursor()
#     sql = "SELECT TuneApple$TuneProd.tune_admin_product.series_id, TuneApple$TuneProd.tune_admin_seriescategory.category " \
#           " FROM TuneApple$TuneProd.tune_admin_product, TuneApple$TuneProd.tune_admin_seriescategory " \
#           " WHERE TuneApple$TuneProd.tune_admin_product.series_id = TuneApple$TuneProd.tune_admin_seriescategory.id AND sell != 1;"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_current_product')
#     cursor.close()
#     return result


# def get_series(name_series):
#     cursor = connect.cursor()

#     sql = f"SELECT category FROM TuneApple$TuneProd.tune_admin_seriescategory WHERE TuneApple$TuneProd.tune_admin_seriescategory.category LIKE '%{name_series}%'"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_series')
#     cursor.close()
#     return result


# def get_detail_product(name_product):
#     cursor = connect.cursor()
#     sql = f"SELECT * FROM TuneApple$TuneProd.tune_admin_product WHERE name = '{name_product}'"
#     cursor.execute(sql)
#     result = cursor.fetchall()[0]
#     print('-------------get_detail_product')
#     cursor.close()
#     return result



# def get_models(name_model):
#     cursor = connect.cursor()
#     sql = f"SELECT * FROM TuneApple$TuneProd.tune_admin_product WHERE name = '{name_model}'"
#     cursor.execute(sql)
#     result = cursor.fetchall()[0]
#     print('-------------get_models')
#     cursor.close()
#     return result


# def get_not_category():
#     cursor = connect.cursor()
#     sql = "SELECT name FROM TuneApple$TuneProd.tune_admin_product WHERE category_id = 6"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     result = [x[0] for x in result]
#     print('-------------get_not_category')
#     cursor.close()
#     return result


# def get_actual_price(name_type):
#     cursor = connect.cursor()
#     sql = f"SELECT * FROM TuneApple$TuneProd.tune_admin_actualprice WHERE type = '{name_type}'"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_actual_price')
#     cursor.close()
#     return result


# def get_all_products():
#     cursor = connect.cursor()
#     sql = "SELECT name FROM TuneApple$TuneProd.tune_admin_product WHERE sell != 1"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print('-------------get_all_products')
#     cursor.close()
#     return result


# cursor = connect.cursor()
# current_category = list(set([x[1] for x in get_current_product()]))
# all_products = [x[0] for x in get_all_products()]
# cursor.close()

# @client.message_handler(func=lambda message: message.text == '⬅️Главное меню')
# @client.message_handler(commands=['start'])
# def start_message(message, text='Что хотите найти?'):
#     print('-------------start_message')
#     start_category = [['Б/У устройства'], ['Купить новое'], ['Trade-in'], ['Мой бюджет'], ['Связаться с менеджером']]
#     keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_category.keyboard = start_category
#     client.send_message(chat_id=message.chat.id,
#                         text=text,
#                         reply_markup=keyboard_category)


# @client.message_handler(commands=['sm'])
# @client.message_handler(func=lambda message: message.text == 'Б/У устройства')
# @client.message_handler(func=lambda message: message.text == '⬅️Назад к Б/У')
# def support_menu(message, text='Вот все Б\У'):
#     print('-------------support_menu')
#     keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_category.keyboard = [[x] for x in menu_support]
#     client.send_message(chat_id=message.chat.id,
#                         text=text,
#                         reply_markup=keyboard_category)


# @client.message_handler(func=lambda message: message.text in menu_support)
# @client.message_handler(func=lambda message: " ".join(message.text.split()[1:5]) in sup_callback)
# def support_models(message):
#     print('-------------support_models')
#     """
#     Покажет все модели в наличии
#     :param message:
#     :return:
#     """

#     print('---', current_category, all_products)
#     if len(message.text.split()) <= 2:
#         model = message.text.split()[1]
#     else:
#         xxx = message.text.split()
#         model = xxx[4]
#     try:
#         models = [[x[0]] for x in get_series(model) if x[0] in current_category]
#     except:
#         models = []
#     if models == []:
#         try:
#             models = [[x[0]] for x in get_series(model) if x[0] in current_category]
#             print('+++++', models)
#             if models == []:
#                 support_menu(message, text='В этой категори сейчас пусто😔\n'
#                                       'Следите за обнавлениями у нас в канале\n'
#                                       'https://t.me/tuneapple 👈')
#         except:
#             print('==========',model, models)
#             return 0

#     models.append(['⬅️Назад к Б/У'])
#     keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_category.keyboard = models
#     client.send_message(chat_id=message.chat.id,
#                         text=f'Вот что есть из {model}',
#                         reply_markup=keyboard_category)


# @client.message_handler(func=lambda message: message.text in current_category)
# def support_products(message):
#     print('-------------support_products')
#     print(message)
#     """
#     Отправка клавиатуры наличия моделей по выброной модели/ серии
#     :param message:
#     :return:
#     """
#     try:
#         products = [[x[1]] for x in get_products(message.text)]
#     except:
#         time.sleep(2)
#         products = [[x[1]] for x in get_products(message.text)]
#     products.sort()
#     if message.text in get_not_category():
#         products.append(['⬅️  Назад к Б/У устройствам'])
#     else:
#         products.append([f'⬅️  Назад к Б/У {message.text.split()[0]}'])

#     keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_products.keyboard = products
#     client.send_message(chat_id=message.chat.id,
#                         text='Ищу: ' + message.text,
#                         reply_markup=keyboard_products)


# @client.message_handler(func=lambda message: message.text in all_products)
# def show_model(message):
#     print('-------------show_model')

#     name = message.text.split()
#     name = name[0] + ' ' + name[1][0]
#     print(name)
#     products = [x[1] for x in get_products_a(name)]
#     print(products)
#     if message.text in products:
#         print(1)
#         products.remove(message.text)
#     print(products)
#     products.sort()
#     products = [[x] for x in products]
#     products.append(['Забронировать|Узнать подробней' + '\n' + message.text])
#     if message.text in get_not_category():
#         products.append(['⬅️  Назад к Б/У Устройства'])
#     else:
#         products.append(['⬅️  Назад к Б/У ' + message.text.split()[0]])
#     keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard.keyboard = products
#     detail_product = get_detail_product(message.text)
#     print(detail_product[1])
#     f1, f2, f3 = open('/home/TuneApple/tune/media/' + detail_product[1], 'rb'), \
#                  open('/home/TuneApple/tune/media/' + detail_product[2], 'rb'), \
#                  open('/home/TuneApple/tune/media/' + detail_product[3], 'rb')
#     f1, f2, f3 = f1.read(), f2.read(), f3.read()

#     client.send_media_group(chat_id=message.chat.id, media=[
#         telebot.types.InputMediaPhoto(f1, caption=detail_product[15]),
#         telebot.types.InputMediaPhoto(f2),
#         telebot.types.InputMediaPhoto(f3), ])
#     # keyboard1 = types.InlineKeyboardMarkup(row_width=2)
#     # buttons = [
#     #     types.InlineKeyboardButton(text="🔥", callback_data="num_decr"),
#     #     types.InlineKeyboardButton(text="👎", callback_data="num_incr"),
#     #     types.InlineKeyboardButton(text="👍", callback_data="num_finish")
#     # ]
#     # keyboard.add(buttons)
#     # client.send_message(chat_id=message.chat.id,
#     #                     text='Хотите забронировать эту модель?',
#     #                     reply_markup=keyboard1)
#     client.send_message(chat_id=message.chat.id,
#                         text='Хотите забронировать эту модель?',
#                         reply_markup=keyboard)


# @client.message_handler(commands=['nm'])
# @client.message_handler(func=lambda message: message.text == 'Купить новое')
# def new_models(message):
#     start_message(message, text='Находится в разработке👨‍💻')


# @client.message_handler(commands=['ti'])
# @client.message_handler(func=lambda message: message.text == 'Trade-in')
# def tradein_model(message):
#     start_message(message, text='Находится в разработке👨‍💻')


# @client.message_handler(commands=['mb'])
# @client.message_handler(func=lambda message: message.text == 'Мой бюджет')
# def show_del(message):
#     start_message(message, text='Находится в разработке👨‍💻')




# # @client.message_handler(content_types=['text'])
# # def bitrix_client(message):

# #     try:
# #         jsn = message.__dict__.get('json')
# #         print('-----', message)
# #         ts = {'update_id': 287246100,
# #               'message': {'message_id': jsn['message_id'],
# #                           'from': {'id': jsn['from']['id'],
# #                                   'is_bot': False,
# #                                   'first_name': jsn['from']['first_name'],
# #                                   'language_code': jsn['from']['language_code']},
# #                           'chat': {'id': jsn['chat']['id'],
# #                                   'first_name': jsn['chat']['first_name'],
# #                                   'type': jsn['chat']['type']},
# #                           'date': jsn['date'],
# #                           'text': jsn['text']}}

# #         requests.post(URL_BITRIX, json=ts)
# #         print(message.text.lower().split()[0])
# #         if message.text.lower().split()[0] == 'забронировать|узнать' or \
# #                 message.text.lower() == 'купить новое устройство':
# #             start_message(message, text='Пожалуйста дождитесь ответа менеджера,'
# #             'он поможет вам забронировать устройство или расскажет о нем более подробно 👩🏻‍💻')
# #         if message.text.lower() == 'связаться с менеджером':
# #             start_message(message, text='Через несколько минут с вами свяжется менеджер\n'
# #                             'Пожалуйста, ожидайте')
# #     except Exception as _:
# #         try:
# #             jsn = message.__dict__.get('json')
# #             ts = {'update_id': 287246100,
# #                   'message': {'message_id': jsn['message_id'],
# #                               'from': {'id': jsn['from']['id'],
# #                                       'is_bot': False,
# #                                       'first_name': jsn['from']['first_name'],
# #                                       'language_code': jsn['from']['language_code']},
# #                               'chat': {'id': jsn['chat']['id'],
# #                                       'first_name': jsn['chat']['first_name'],
# #                                       'type': jsn['chat']['type']},
# #                               'date': jsn['date'],
# #                               'text': jsn['text']}}

# #             requests.post(URL_BITRIX, json=ts)
# #             start_message(message, text='Я вас не понимаю 🙄\n'
# #                                         'Напишите еще раз')
# #         except:
# #             start_message(message, text='Произошла ошибка телеграмма 🙄\n'
# #                                         'Попробуйте написать через 5 минут'
# #                                         'Или напишите нашему менеджеру — Виктории @VasViktory')

# # @client.message_handler(content_types=['photo'])
# # def photo(message):
# #     jsn = message.__dict__.get('json')
# #     exit_dict = {"update_id": 287246100} | {"message":jsn}
# #     requests.post(URL_BITRIX, json=exit_dict)











