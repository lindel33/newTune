from pprint import pprint
import datetime
import MySQLdb
import telebot
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied
import requests
from .models import Product, Category, SeriesCategory
from cost_models.models import DetailModel


TOKEN = '5239855839:AAG6A81Vv1BjQr1HnGtIJHxQ1rbKSc3QBs4'
<<<<<<< HEAD
URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/6c529968ec581a32c38753edca1c926a1645891257/'

=======

URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/6c529968ec581a32c38753edca1c926a164589125227/'
>>>>>>> 7cfad682a4aefd882fc86159539124b16ef59a02
client = telebot.TeleBot(TOKEN, threaded=False)
menu_support = ['📱 iPhone', '📲 iPad', '💻 MacBook',
                '🎧 AirPods', '⌚ Watch',
                '⌨ Устройства', '⬅️Главное меню']
sup_callback = ['Назад к Б/У iPhone', 'Назад к Б/У iPad', 'Назад к Б/У MacBook',
                'Назад к Б/У AirPods', 'Назад к Б/У Watch',
                'Назад к Б/У Устройства']

path_to_media = '/home/apple/code/project1/tune/media/'


@csrf_exempt
def bot(request):

    if request.META['CONTENT_TYPE'] == 'application/json':
        try:

            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            client.process_new_updates([update])
            print('-----------------------4')
            return HttpResponse({'200': 'ok'})

        except:

            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            client.process_new_updates([update])
            print('+++++++++++++++++++++++4')
            return HttpResponse({'200': 'ok'})

    else:
        raise HttpResponse({'200': 'ok'})


def get_category():
    result = ['📱 iPhone','📲 iPad','💻 MacBook','🎧 AirPods','⌚ Watch','⌨ Устройства']
    return result


def get_series(name_series):
    result = SeriesCategory.objects.filter(category__icontains=f'{name_series}')
    list_1 = []
    for i in result:
        list_1.append(i.category)
    return list_1


def get_detail_product(name_product):
    result = Product.objects.filter(name=f'{name_product}')
    return result


def get_not_category():
    result = Product.objects.all().filter(category_id=6)
    list_device = []
    for r in result:
        list_device.append(r.name)
    return list_device

def get_all_products():
    result = Product.objects.values('name').filter(sell=False).filter(booking=False).filter(moderation=True)
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all

def max_all_products():
    result = Product.objects.values('name')
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all

def get_current_product():
    result = Product.objects.values('series_id').filter(sell=False).filter(booking=False).filter(moderation=True)
    list_id = []
    exit = []
    for i in result:
        list_id.append(i['series_id'])
    for i in list_id:
        result = SeriesCategory.objects.values('category').filter(id=i)
        exit.append(result[0]['category'])
    return list(set(exit))


def get_products(category_name):
    id_category = SeriesCategory.objects.values('id').filter(category__icontains=f'{category_name}')
    result = Product.objects.values('name').filter(series_id=id_category[0]['id']).filter(booking=False).filter(sell=False).filter(moderation=True)
    list_product = []
    for i in result:
        list_product.append(i['name'])
    return list_product


def get_price(price_min, price_max):
    result = Product.objects.values('name').filter(price__gte=price_min, price__lte=price_max).filter(name__icontains=f'{"iPhone"}').filter(booking=False).filter(sell=False).filter(moderation=True)
    result = [['⋅ '+ str(x['name'])] for x in result]
    print(result)
    return result

def get_max_min_price(cost):
    dia = [[15000, 25000],
             [25000, 35000],
             [35000, 45000],
             [45000, 55000],
             [55000, 70000],
             [70000, 100000]]
    for i in dia:
        if i[0] <= cost <= i[1]:
            return [i[0], i[1]]

def get_sale():
    result = Product.objects.values('name').\
        filter(sell=False).\
        filter(booking=False).\
        filter(moderation=True).\
        filter(sale=True)
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all
  
  
current_category = list(set([x[1] for x in get_current_product()]))
all_products = [x for x in get_all_products()]
current_product = get_current_product()
max_products = [x for x in max_all_products()]


@client.message_handler(func=lambda message: message.text == 'Запуск')
@client.message_handler(func=lambda message: message.text == 'Начало')
@client.message_handler(func=lambda message: message.text == 'Запустить бота')
@client.message_handler(func=lambda message: message.text == 'Начать')
@client.message_handler(func=lambda message: message.text == 'Старт')
@client.message_handler(func=lambda message: message.text == '⬅️Главное меню')
@client.message_handler(commands=['start'])
def start_message(message, text='Что хотите найти?'):
    start_category = [['💥Скидки💥'], ['Б/У Устройства'],['Новые Устройства'], ['Trade-in'], ['Мой бюджет'], ['Связаться с менеджером']]
    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = start_category
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard_category)


@client.message_handler(commands=['sm'])
@client.message_handler(func=lambda message: message.text == 'Б/У Устройства')
@client.message_handler(func=lambda message: message.text == '⬅️Назад к Б/У')
def support_menu(message, text='Вот все Б\У'):
    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = [[x] for x in menu_support]
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard_category)


@client.message_handler(func=lambda message: message.text == '⌨ Устройства')
def supp_product(message):
    """
    Обратока для Б\У
    """
    products = [[x] for x in get_products(message.text.split()[1])]
    products.sort()
    if message.text in get_not_category():
        products.append(['⬅️  Назад к Б/У Устройствам'])
    else:
        products.append(['⬅️Назад к Б/У'])

    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = products
    client.send_message(chat_id=message.chat.id,
                        text='Ищу: ' + message.text,
                        reply_markup=keyboard_products)



@client.message_handler(func=lambda message: message.text in menu_support)
@client.message_handler(func=lambda message: " ".join(message.text.split()[1:5]) in sup_callback)
def support_models(message):
    """
    Покажет все модели в наличии
    :param message:
    :return:
    """

    if len(message.text.split()) <= 2:
        model = message.text.split()[1]
    else:
        xxx = message.text.split()
        model = xxx[4]

    models = [x for x in get_series(model) if x in current_product]
    if models == 'iPhone':
        bce = ['iPhone 5', 'iPhone 6 / 6+ / 6s / 6s+',
     'iPhone 7 / 7+', 'iPhone 8 / 8+',
     'iPhone X / XS / XS Max', 'iPhone 11 / Pro / Max',
     'iPhone 12 / Pro / Max / Mini', 'iPhone 13 / Pro / Max / Mini',
     'iPhone SE / XR']

        ect = models.copy()

        models = bce
        x = bce.copy()
        for b in ect:
            if b in x:
                x.remove(b)
        for i in x:
            models.remove(i)

    if models == []:
        support_menu(message, text='В этой категори сейчас пусто😔\n'
                               'Следите за обнавлениями у нас в канале\n'
                               'https://t.me/tuneapple 👈')

        return 0

    models = [[x] for x in models]

    models.append(['⬅️Назад к Б/У'])
    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = models
    client.send_message(chat_id=message.chat.id,
                        text=f'Вот что есть из {model}',
                        reply_markup=keyboard_category)


@client.message_handler(func=lambda message: message.text in current_product)
def support_products(message):
    """
    Отправка клавиатуры наличия моделей по выброной модели/ серии
    :param message:
    :return:
    """
    print(message.chat.id)
    products = [x for x in get_products(message.text)]

    products.sort()
    products = [[x] for x in products]

    if message.text in get_not_category():
        products.append(['⬅️  Назад к Б/У Устройствам'])
    else:
        products.append([f'⬅️  Назад к Б/У {message.text.split()[0]}'])

    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = products
    client.send_message(chat_id=message.chat.id,
                        text='Ищу: ' + message.text,
                        reply_markup=keyboard_products)


dig = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]
@client.message_handler(func=lambda message: message.text in all_products)
@client.message_handler(func=lambda message: '⋅' in message.text)
@client.message_handler(func=lambda message: message.text.split()[0] == '🔻')
def show_model(message, extra=None):
    tmp = message.text
    name_to_search = message.text
    try:
        name = message.text.split()
        if name[0] == '⋅':
            name.remove('⋅')
        if '⋅' in message.text:
            name_to_search = message.text.replace('⋅ ', '')
        
        if name[0] == '🔻':
          name.remove('🔻')
        if '🔻' in message.text:
          name_to_search = message.text.replace('🔻 ', '')
        print('--', name)
        name1 = name[0] + ' ' + name[1][0]
        products = []


        if len(name[1]) > 1 or message.text in get_not_category():

            if message.text in get_not_category():

                products = get_not_category()
            elif (name[1][0] + name[1][1] == 'XR' or name[1][0] + name[1][
                1] == 'SE') and 'watch' not in message.text.lower():

                xr = name[1][0] + name[1][1]
                products = get_products(xr)
            elif name[1][0] in dig and name[1][1] in dig:

                name_11 = name[0] + ' ' + name[1]
                products = get_products(name_11)
            else:
                products = get_products(name1)

        if len(name[1]) == 1 and message.text not in get_not_category():
            products = get_products(name1)

        if message.text in products:
            products.remove(message.text)

        detail_product = get_detail_product(name_to_search)
        print('___+++', name_to_search)
        if '⋅' in tmp:
            current_price = get_max_min_price(detail_product[0].price)
            products = get_price(current_price[0], current_price[1])
            if [tmp] in products:
                products.remove([tmp])
                products.append(['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. '+detail_product[0].article])
            products.append(['⬅️Другой бюджет'])
        
        elif '🔻' in tmp:
          products = [['🔻 ' + x] for x in get_sale()]
          if [tmp] in products:
              products.remove([tmp])
              products.append(['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
          products.append(['⬅️Главное меню'])
          
        else:
            products = [[x] for x in products]
            products.append(['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. '+detail_product[0].article])
            if message.text in get_not_category():
                products.append(['⬅️Назад к Б/У ' + ''])
            else:
                products.append(['⬅️  Назад к Б/У ' + message.text.split()[0]])
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.keyboard = products

        if detail_product[0].image_3:
            f1, f2, f3 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_2), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_3), 'rb')
            f1, f2, f3 = f1.read(), f2.read(), f3.read()
            client.send_media_group(chat_id=message.chat.id, media=[
                telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text),
                telebot.types.InputMediaPhoto(f2),
                telebot.types.InputMediaPhoto(f3), ])
            client.send_message(chat_id=message.chat.id,
                                text='Хотите забронировать эту модель?',
                                reply_markup=keyboard)
        else:
            f1, f2 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_2), 'rb')

            f1, f2 = f1.read(), f2.read()
            client.send_media_group(chat_id=message.chat.id, media=[
                telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text),
                telebot.types.InputMediaPhoto(f2)])
            client.send_message(chat_id=message.chat.id,
                                text='Хотите забронировать эту модель?',
                                reply_markup=keyboard)
    except:
        return 0








@client.message_handler(commands=['nm'])
@client.message_handler(func=lambda message: message.text == 'Новые Устройства')
def new_model(message):
    start_message(message, text='Новые устройства всегда в наличии.\nДля заказа выберите пункт «Связаться с менеджером»\nИли позвоните по телефону: \n+7 (932) 222-54-45')



# def get_new_products():
#     try:
#         result = DetailModel.objects.values('series')

#         result = [x['series'] for x in result]
#         result = sorted(list(set(result)))
#         return result
#     except:
#         pass


# @client.message_handler(commands=['nm'])
# @client.message_handler(func=lambda message: message.text == 'Новые Устройства')
# @client.message_handler(func=lambda message: message.text == '⬅️ Назад новым устройствам')
# def new_models(message):
#     try:
#         keyboard_new_products = [['🆕 iPhone'], ['⬅️Главное меню']]
#         keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#         keyboard_category.keyboard = keyboard_new_products
#         client.send_message(chat_id=message.chat.id,
#                             text='Доступные категории',
#                             reply_markup=keyboard_category)

#     except:
#         pass
# @client.message_handler(func=lambda message: message.text.split()[0] == '🆕')
# @client.message_handler(func=lambda message: '⬅️ Назад новым' in message.text)
# def new_models2(message):
#     try:
#         if message.text.split()[0] == '🆕':
#             model = message.text.split()[1]
#         else:
#             model = message.text.split()[3]
#         keyboard_new_products = [[f'✔ {model} ' + x] for x in get_new_products()]
#         keyboard_new_products.append(['⬅️ Назад новым устройствам'])
#         keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#         keyboard_category.keyboard = keyboard_new_products
#         client.send_message(chat_id=message.chat.id,
#                             text='Какая серия Вам интересна?',
#                             reply_markup=keyboard_category)

#     except:
#         pass


# def get_price_new(series):
#     try:
#         result = DetailModel.objects.filter(series=series)

#         result = [x['series'] for x in result]
#         result = sorted(list(set(result)))
#         return result
#         correct = {
#             'iphone': 'iPhone',
#             'macbook': 'MacBook',

#         }
#         correct_list = ['iphone', 'macbook']
#         exit_list = []
#         for i in result:

#             for j in correct_list:
#                 if j in i:
#                     i = i.replace(j, correct.get(j))
#                     exit_list.append(i)
#         return list(set(exit_list))
#     except:
#         pass

# @client.message_handler(func=lambda message: message.text.split()[0] == '✔')
# def new_models3(message):
#     try:
#         model = message.text.split()[1]
#         series = message.text.replace('✔ ', '')
#         series = series.replace('iPhone ', '')
#         series = get_price_new(series)
#         keyboard_new_price = [['Заказать ' + x] for x in series]
#         keyboard_new_price.append(['Связаться с менеджером'])
#         keyboard_new_price.append([f'⬅️ Назад новым {model}'])
#         keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
#         keyboard_category.keyboard = keyboard_new_price
#         client.send_message(chat_id=message.chat.id,
#                             text=f'Актуально на {datetime.date.today().strftime("%d.%m.%Y")}:'
#                                  f'\n\n{"".join(series)}',
#                             reply_markup=keyboard_category)
#         client.send_message(chat_id=message.chat.id,
#                             text='Для заказа выберите модель\n'
#                                  'Если Вы не увидели интересующей модели свяжитесь с менеджером',
#                             reply_markup=keyboard_category)
#     except:
#         pass






@client.message_handler(commands=['mb'])
@client.message_handler(func=lambda message: message.text == 'Мой бюджет')
@client.message_handler(func=lambda message: message.text == '⬅️Другой бюджет')
def my_budget(message, text='Выберите бюджет'):
    my_dia = [['Бюджет от 15000 до 25000'],
              ['Бюджет от 25000 до 35000'],
              ['Бюджет от 35000 до 45000'],
              ['Бюджет от 45000 до 55000'],
              ['Бюджет от 55000 до 70000'],
              ['Бюджет от 70000 до 100000'],
              ['⬅️Главное меню']]
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = my_dia
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)





@client.message_handler(func=lambda message: message.text.split()[0] == 'Бюджет')
def my_budget_show(message):
    if len(message.text.split()) >= 4:
        try:
            price_min = message.text.split()[2]
            price_max = message.text.split()[4]
            keyboard_products = get_price(price_min, price_max)

            if keyboard_products == []:
                my_budget(message, 'Ничего не найдено')
                return 0
            keyboard_products.sort()
            keyboard_products.append(['⬅️Другой бюджет'])

            keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard_category.keyboard = keyboard_products
            client.send_message(chat_id=message.chat.id,
                                text='Вот ссылки на все модели по Вашему бюджету',
                                reply_markup=keyboard_category)
        except:
            pass

@client.message_handler(commands=['sale'])
@client.message_handler(func=lambda message: message.text == '💥Скидки💥')
def tradein_model(message):
    sale = get_sale()
    result = [['🔻 ' + x] for x in sorted(sale)]
    result.append(['⬅️Главное меню'])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = result
    client.send_message(chat_id=message.chat.id,
                        text='Вот все скидки',
                        reply_markup=keyboard_products)
          
@client.message_handler(commands=['ti'])
@client.message_handler(func=lambda message: message.text == 'Trade-in')
def tradein_model(message):
    start_message(message, text='Программа trade-in доступна!\nС помощью нее вы можете сдать свое старое устройство Apple и получить скидку на новое или б/у (так же принятое по программе trade-in).\nЧтобы узнать размер скидки выберите пункт «Связаться с менеджером»\nИли позвоните по телефону: \n+7 (932) 222-54-45')

@client.message_handler(content_types=['text'])
def bitrix_client(message):
    if message.text not in max_products:
        if message.text.split()[0] != 'Бюджет':
            try:
                print('---', message.text)
                jsn = message.__dict__.get('json')

                ts = {'update_id': 287246100,
                      'message': {'message_id': jsn['message_id'],
                                  'from': {'id': jsn['from']['id'],
                                          'is_bot': False,
                                          'first_name': jsn['from']['first_name'],
                                          'language_code': jsn['from']['language_code']},
                                  'chat': {'id': jsn['chat']['id'],
                                          'first_name': jsn['chat']['first_name'],
                                          'type': jsn['chat']['type']},
                                  'date': jsn['date'],
                                  'text': jsn['text']}}

                requests.post(URL_BITRIX, json=ts)

                if 'забронировать|узнать' in message.text.lower() or \
                        message.text.lower() == 'купить новое устройство':
                    start_message(message, text='Пожалуйста дождитесь ответа менеджера,'
                    ' он поможет Вам забронировать устройство или расскажет о нем более подробно 👩🏻‍💻')
                if message.text.lower() == 'связаться с менеджером':
                    start_message(message, text='Через несколько минут с Вами свяжется менеджер\n'
                                    'Пожалуйста, ожидайте')
            except Exception as _:
                try:
                    jsn = message.__dict__.get('json')
                    ts = {'update_id': 287246100,
                          'message': {'message_id': jsn['message_id'],
                                      'from': {'id': jsn['from']['id'],
                                              'is_bot': False,
                                              'first_name': jsn['from']['first_name'],
                                              'language_code': jsn['from']['language_code']},
                                      'chat': {'id': jsn['chat']['id'],
                                              'first_name': jsn['chat']['first_name'],
                                              'type': jsn['chat']['type']},
                                      'date': jsn['date'],
                                      'text': jsn['text']}}

                    requests.post(URL_BITRIX, json=ts)
                    start_message(message, text='Я вас не понимаю 🙄\n'
                                                'Напишите еще раз')
                except:
                    start_message(message, text='Произошла ошибка телеграмма 🙄\n'
                                                'Попробуйте написать через 5 минут'
                                                'Или напишите нашему менеджеру — Виктории @VasViktory')

@client.message_handler(content_types=['photo'])
def photo(message):
    jsn = message.__dict__.get('json')
    exit_dict = {"update_id": 287246100} | {"message":jsn}
    requests.post(URL_BITRIX, json=exit_dict)
# # except:
# #     HttpResponse({'200': 'ok'})
