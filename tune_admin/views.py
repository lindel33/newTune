import os
import datetime
import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from trade_in.models import (TelegramUserModel, UserStepModel,
                             TradeInDevicesModel, TradeInSeriesModel,
                             VariableFoeStepModel, TradeInStepModel)
from trade_id.models import (ButtonModel, ServiceModels,
                             UserChoiceModel, UseService)
from tune_admin.models import (Product, SeriesCategory,
                               StaticUserHourModel, UserModel,
                               RegionUserModel, )

TOKEN = '5239855839:AAFeQBXF4EmVJK7DDy6RN9rPeIIgskPWLig'
URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/e5750b73ce4b6f9cbedb96d9d7faf0881653435781/'
client = telebot.TeleBot(TOKEN, threaded=False)

menu_support = ['📱 iPhone', '📲 iPad', '💻 MacBook',
                '🎧 AirPods', '⌚ Watch',
                '⬅️Главное меню']
#'⌨ Устройства', 
sup_callback = ['Назад к Б/У iPhone', 'Назад к Б/У iPad', 'Назад к Б/У MacBook',
                'Назад к Б/У AirPods', 'Назад к Б/У Watch',
                'Назад к Б/У Устройства']
path_to_media = '/home/apple/code/project1/tune/media/'


def get_category():
    result = ['📱 iPhone', '📲 iPad', '💻 MacBook', '🎧 AirPods', '⌚ Watch',]
    return result

# '⌨ Устройства'
def get_series(name_series):
    result = SeriesCategory.objects.filter(category__icontains=f'{name_series}')
    list_1 = []
    for i in result:
        list_1.append(i.category)
    return list_1


def get_detail_product(name_product):
    result = Product.objects.filter(name=f'{name_product}')
    return result


def get_trade_state(name_to_search):
    result = Trade.objects.filter(name_button=f'{name_to_search}')
    return result


def get_not_category(message):
    result = Product.objects.filter(category_id=6,
                                    regin=UserModel.objects.get(
                                        user_id=message.chat.id
                                    ).region_user
                                    )
    list_device = []
    for r in result:
        list_device.append(r.name)
    return list_device


def get_all_products():
    result = [i[0] for i in Product.objects.values_list('name').filter(sell=False,
                                                                       booking=False,
                                                                       moderation=True,
                                                                       )]

    return result


def max_all_products(message):
    result = Product.objects.values('name')
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


def get_current_product(message):
    result = Product.objects.values('series_id').filter(sell=False,
                                                        booking=False,
                                                        moderation=True,
                                                        regin=UserModel.objects.get(
                                                            user_id=message.chat.id
                                                        ).region_user)
    list_id = []
    exit = []
    for i in result:
        list_id.append(i['series_id'])
    for i in list_id:
        result = SeriesCategory.objects.values('category').filter(id=i)
        exit.append(result[0]['category'])
    return list(set(exit))


def get_products(category_name, message):
    id_category = SeriesCategory.objects.values('id').filter(category__icontains=f'{category_name}')
    result = Product.objects.values('name').filter(series_id=id_category[0]['id'],
                                                   moderation=True,
                                                   booking=False,
                                                   sell=False,
                                                   regin=UserModel.objects.get(
                                                       user_id=message.chat.id
                                                   ).region_user
                                                   )
    list_product = []
    for i in result:
        list_product.append(i['name'])
    return list_product


def get_price(price_min, price_max, message):
    result = Product.objects.values('name').filter(
        price__gte=price_min,
        price__lte=price_max,
        name__icontains=f'{"iPhone"}',
        booking=False,
        sell=False,
        moderation=True,
        regin=UserModel.objects.get(
            user_id=message.chat.id
        ).region_user)
    result = [['⋅ ' + str(x['name'])] for x in result]
    return result


def get_max_min_price(cost):
    dia = [[1000, 15000],
           [15000, 25000],
           [25000, 35000],
           [35000, 45000],
           [45000, 55000],
           [55000, 70000],
           [70000, 100000],
           [100000, 130000],
           [130000, 200000], ]
    for i in dia:
        if i[0] <= cost <= i[1]:
            return [i[0], i[1]]


def get_sale(message):
    result = Product.objects.values('name').filter(sell=False,
                                                   booking=False,
                                                   sale=True,
                                                   regin=UserModel.objects.get(
                                                       user_id=message.chat.id
                                                   ).region_user)
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


# def global_message(list_user, text):
#     for i in list_user:
#         client.send_message(chat_id=i,
#                             text=text)



@client.message_handler(commands=['set'])
def menu_settings(message):
    user_info = UserModel.objects.get(
        user_id=str(message.chat.id),
    )
    user_notifications = user_info.notifications
    if user_notifications:
        user_notifications = 'Включены'
    else:
        user_notifications = 'Отключены'
    user_region = user_info.region_user
    text = f'Ваши текущие настройки:\n' \
           f'Регион: {user_region}\n' \
           f'Уведомления: {user_notifications}'
    markup_settings = telebot.types.InlineKeyboardMarkup()
    butt = telebot.types.InlineKeyboardButton('Выбор региона', callback_data='region')
    markup_settings.add(butt)
    butt = telebot.types.InlineKeyboardButton('Уведомления', callback_data='notif')
    markup_settings.add(butt)
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=markup_settings)

@client.callback_query_handler(func=lambda call: True)
def switch_region(call):
  
    global_regions = RegionUserModel.objects.all()
    global_regions = [i.name for i in global_regions]
    markup_region = telebot.types.InlineKeyboardMarkup()

    for i in global_regions:
        button = telebot.types.InlineKeyboardButton(str(i), callback_data=str(i))
        markup_region.add(button)
        
    client.send_message(chat_id=572982939,
                        text='Выберите свой регион')
    if call.data == 'region':
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.id,
                                 text='Выберите свой регион',
                                 reply_markup=markup_region)

    if call.data == 'notif':
        markup_notif = telebot.types.InlineKeyboardMarkup()
        but = telebot.types.InlineKeyboardButton('Включить', callback_data='onNotif')
        markup_notif.add(but)
        but = telebot.types.InlineKeyboardButton('Отключить', callback_data='offNotif')
        markup_notif.add(but)
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.id,
                                 text='Выберите свой регион',
                                 reply_markup=markup_notif)

    if call.data in ['onNotif', 'offNotif']:
        if call.data == 'onNotif':
            UserModel.objects.filter(
                user_id=str(call.message.chat.id),
            ).update(notifications=True)
            client.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.id,
                                     text=f'Теперь Вы будете получать уведомления в боте',
                                     )
        if call.data == 'offNotif':
            UserModel.objects.filter(
                user_id=str(call.message.chat.id),
            ).update(notifications=False)
            client.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.id,
                                     text=f'Вы больше не будете получать уведомления в боте',
                                     )

    if call.data in global_regions:
        UserModel.objects.filter(
            user_id=str(call.message.chat.id),
        ).update(region_user=RegionUserModel.objects.get(name=call.data))
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.id,
                                 text=f'Ваш регион изменен на {call.data}',
                                 )

@client.message_handler(func=lambda message: message.text == 'Запуск')
@client.message_handler(func=lambda message: message.text == 'Начало')
@client.message_handler(func=lambda message: message.text == 'Запустить бота')
@client.message_handler(func=lambda message: message.text == 'Начать')
@client.message_handler(func=lambda message: message.text == 'Старт')
@client.message_handler(func=lambda message: message.text == '⬅️Главное меню')
@client.message_handler(commands=['start'])
def start_message(message, text='Что хотите найти?'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('💥Скидки💥')
    btn2 = telebot.types.KeyboardButton('Новые Устройства')
    btn3 = telebot.types.KeyboardButton('Б/У Устройства')
    btn4 = telebot.types.KeyboardButton('Trade-in / Продажа')
    btn5 = telebot.types.KeyboardButton('Мой бюджет')
    # btn6 = telebot.types.KeyboardButton('Обменка')
    # btn7 = telebot.types.KeyboardButton('FAQ')
    btn8 = telebot.types.KeyboardButton('Связаться с менеджером')
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    # markup.add(btn6, btn7)
    markup.add(btn8)
    client.send_message(message.chat.id, text=text, reply_markup=markup)


@client.message_handler(commands=['sm'])
@client.message_handler(func=lambda message: message.text == 'Б/У Устройства')
@client.message_handler(func=lambda message: message.text == '⬅️Назад к Б/У')
def support_menu(message, text='Вот все Б\У'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('📱 iPhone')
    btn2 = telebot.types.KeyboardButton('📲 iPad')
    btn3 = telebot.types.KeyboardButton('💻 MacBook')
    btn4 = telebot.types.KeyboardButton('⌚ Watch')
    btn5 = telebot.types.KeyboardButton('🎧 AirPods')
#     btn8 = telebot.types.KeyboardButton('⌨ Устройства')
    btn9 = telebot.types.KeyboardButton('⬅️Главное меню')
    markup.add(btn1)
    markup.add(btn4, btn5)
    markup.add(btn2, btn3)
#     markup.add(btn8)
    markup.add(btn9)
    client.send_message(message.chat.id, text=text, reply_markup=markup)


@client.message_handler(func=lambda message: message.text == '⌨ Устройства')
def supp_product(message):
    """
    Обратока для Б\У
    """
    products = [[x] for x in get_products(message.text.split()[1],
                                          message=message)]
    products.sort()
    if message.text in get_not_category(message=message):
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

    models = [x for x in get_series(model) if x in get_current_product(message)]
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

    if not models:
        support_menu(message, text='В этой категории сейчас пусто😔\n'
                                   'Следите за обновлениями у нас в канале\n'
                                   'https://t.me/tuneapple 👈')

        return 0

    models = [[x] for x in models]

    models.append(['⬅️Назад к Б/У'])
    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = models
    client.send_message(chat_id=message.chat.id,
                        text=f'Вот что есть из {model}',
                        reply_markup=keyboard_category)


@client.message_handler(func=lambda message: message.text in get_current_product(message))
def support_products(message):
    """
    Отправка клавиатуры наличия моделей по выбранной модели/ серии
    :param message:
    :return:
    """
    products = [x for x in get_products(message.text,
                                        message=message)]

    products.sort()
    products = [[x] for x in products]

    if message.text in get_not_category(message=message):
        products.append(['⬅️  Назад к Б/У Устройствам'])
    else:
        products.append([f'⬅️  Назад к Б/У {message.text.split()[0]}'])

    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = products
    client.send_message(chat_id=message.chat.id,
                        text='Ищу: ' + message.text,
                        reply_markup=keyboard_products)


dig = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]


def get_trade_state(name_to_search):
    result = Trade.objects.filter(name_button=f'{name_to_search}')
    return result


@client.message_handler(func=lambda message: message.text in [x for x in get_all_products()])
@client.message_handler(func=lambda message: '⋅' in message.text)
@client.message_handler(func=lambda message: message.text.split()[0] == '🔻')
def show_model(message):
    tmp = message.text
    name_to_search = message.text
    name = message.text.split()
    if name[0] == '⋅':
        name.remove('⋅')
    if '⋅' in message.text:
        name_to_search = message.text.replace('⋅ ', '')

    if name[0] == '🔻':
        name.remove('🔻')
    if '🔻' in message.text:
        name_to_search = message.text.replace('🔻 ', '')

    if name[0] == '🔁':
        name.remove('🔁')
    if '🔁' in message.text:
        name_to_search = message.text.replace('🔁 ', '')
    name1 = name[0] + ' ' + name[1][0]
    products = []

    if '🔁' not in message.text and \
            len(name[1]) > 1 or message.text in get_not_category(message=message):

        if message.text in get_not_category(message=message):

            products = get_not_category(message=message)
        elif (name[1][0] + name[1][1] == 'XR' or name[1][0] +
              name[1][1] == 'SE') and 'watch' not in message.text.lower():

            xr = name[1][0] + name[1][1]
            products = get_products(xr,
                                    message=message)
        elif name[1][0] in dig and name[1][1] in dig:

            name_11 = name[0] + ' ' + name[1]
            products = get_products(name_11,
                                    message=message)
        else:
            products = get_products(name1,
                                    message=message)

    if len(name[1]) == 1 and message.text not in get_not_category(message=message):
        products = get_products(name1,
                                message=message)

    if message.text in products:
        products.remove(message.text)

    detail_product = get_detail_product(name_to_search)
    if '⋅' in tmp:
        current_price = get_max_min_price(detail_product[0].price)
        products = get_price(current_price[0], current_price[1], message)
        if [tmp] in products:
            products.remove([tmp])
            products.insert(0,
                            ['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. ' + detail_product[
                                0].article])
        products.append(['⬅️Другой бюджет'])

    elif '🔻' in tmp:
        products = [['🔻 ' + x] for x in get_sale(message)]
        if [tmp] in products:
            products.remove([tmp])
            products.insert(0,
                            ['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
        products.append(['⬅️Главное меню'])

    elif '🔁' in tmp:
        detail_product = get_trade_state(name_to_search)
        products = [['🔁 ' + x.name_button] for x in Trade.objects.all()]
        if [tmp] in products:
            products.remove([tmp])
            products.insert(0,
                            ['Забронировать|Узнать подробней' + '\n' + tmp])
        products.append(['⬅️Главное меню'])

    else:
        products = [[x] for x in products]
        products.insert(0,
                        ['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. ' + detail_product[
                            0].article])
        if message.text in get_not_category(message=message):
            products.append([['⬅️Назад к Б/У ' + '']])
        else:
            products.append(['⬅️  Назад к Б/У ' + message.text.split()[0]])
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = products
    if '🔁' not in tmp:
        if detail_product[0].image_3:
            f1, f2, f3 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                         open(path_to_media + str(detail_product[0].image_2), 'rb'), \
                         open(path_to_media + str(detail_product[0].image_3), 'rb')
            f1, f2, f3 = f1.read(), f2.read(), f3.read()
            client.send_media_group(chat_id=message.chat.id, media=[
                telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text, parse_mode='HTML'),
                telebot.types.InputMediaPhoto(f2),
                telebot.types.InputMediaPhoto(f3), ])
            client.send_message(chat_id=message.chat.id,
                                text='Хотите забронировать эту модель?',
                                reply_markup=keyboard,
                                parse_mode='HTML')
            return 0
        else:
            f1, f2 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_2), 'rb')

            f1, f2 = f1.read(), f2.read()
            client.send_media_group(chat_id=message.chat.id, media=[
                telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text, parse_mode='HTML'),
                telebot.types.InputMediaPhoto(f2)])
            client.send_message(chat_id=message.chat.id,
                                text='Хотите забронировать эту модель?',
                                reply_markup=keyboard,
                                parse_mode='HTML')
            return 0
    else:
        f1 = open(path_to_media + str(detail_product[0].image_1), 'rb')
        f2 = open(path_to_media + str(detail_product[0].image_2), 'rb')

        f1, f2 = f1.read(), f2.read()
        client.send_media_group(chat_id=message.chat.id, media=[
            telebot.types.InputMediaPhoto(f1, caption=detail_product[0].text, parse_mode='HTML'),
            telebot.types.InputMediaPhoto(f2)])
        client.send_message(chat_id=message.chat.id,
                            text='Хотите узнать подробнее?',
                            reply_markup=keyboard,
                            parse_mode='HTML')
        return 0


@client.message_handler(commands=['nm'])
@client.message_handler(func=lambda message: message.text == 'Новые Устройства')
def new_model(message):
    client.send_message(chat_id=message.chat.id,
                        text='https://tuneapple.ru',
                        parse_mode='HTML')


@client.message_handler(commands=['mb'])
@client.message_handler(func=lambda message: message.text == 'Мой бюджет')
@client.message_handler(func=lambda message: message.text == '⬅️Другой бюджет')
def my_budget(message, text='Выберите бюджет'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('от 1000 до 15000')
    btn2 = telebot.types.KeyboardButton('от 15000 до 25000')
    btn3 = telebot.types.KeyboardButton('от 25000 до 35000')
    btn4 = telebot.types.KeyboardButton('от 45000 до 55000')
    btn5 = telebot.types.KeyboardButton('от 55000 до 70000')
    btn6 = telebot.types.KeyboardButton('от 70000 до 100000')
    btn7 = telebot.types.KeyboardButton('от 100000 до 130000')
    btn8 = telebot.types.KeyboardButton('от 130000 до 200000')
    btn9 = telebot.types.KeyboardButton('⬅️Главное меню')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    markup.add(btn9)
    client.send_message(message.chat.id, text=text, reply_markup=markup)


@client.message_handler(func=lambda message: message.text.split()[0] == 'от')
def my_budget_show(message):
    if len(message.text.split()) >= 4:
        try:
            price_min = message.text.split()[1]
            price_max = message.text.split()[3]
            keyboard_products = get_price(price_min, price_max, message)

            if not keyboard_products:
                my_budget(message, 'Ничего не найдено')
                return 0
            keyboard_products.sort()
            keyboard_products.append(['⬅️Другой бюджет'])

            keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard_category.keyboard = keyboard_products
            client.send_message(chat_id=message.chat.id,
                                text='Вот ссылки на все модели по Вашему бюджету',
                                reply_markup=keyboard_category,
                                parse_mode='MarkdownV2')
        except EnvironmentError as _:
            pass


from faq.models import FAQModel

faq_info = FAQModel.objects.all()
buttons_info = [['💡 ' + i.name] for i in faq_info]
buttons_info.append(['⬅️Главное меню'])


@client.message_handler(func=lambda message: message.text == 'FAQ')
def main_menu_faq(message, text='Выберите раздел FAQ'):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = buttons_info
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text.split()[0] == '💡')
def main_menu_faq(message):
    text_message = message.text.replace('💡 ', '')
    info = None
    for i in faq_info:
        if i.name == text_message:
            info = i
            break

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = buttons_info
    if info.image:
        photos = open(path_to_media + str(info.image), 'rb')
        photos = photos.read()
        client.send_photo(
            chat_id=message.chat.id,
            caption=info.text,
            photo=photos,
            reply_markup=keyboard,
        )
    if not info.image:
        client.send_message(chat_id=message.chat.id,
                            text=info.text,
                            reply_markup=keyboard)


main_menu = TradeInDevicesModel.objects.all()
main_menu = [[buttons.name] for buttons in main_menu]
main_menu.append(['⬅️Главное меню'])


@client.message_handler(commands=['ti'])
@client.message_handler(func=lambda message: message.text == '⬅️Назад к Trade-in')
@client.message_handler(func=lambda message: message.text == 'Trade-in / Продажа')
def trade_main(message, text='Выберите устройство'):
    start_message(message, text='Программа trade-in доступна!\nС помощью нее вы можете сдать свое старое устройство Apple и получить скидку на новое или б/у (так же принятое по программе trade-in).\nЧтобы узнать размер скидки выберите пункт «Связаться с менеджером»\nИли позвоните по телефону: \n+7 (932) 222-54-45')
  
#     list_user = UserModel.objects.all()
#     list_user_id = [str(user_id.user_id) for user_id in list_user]

#     id_user = message.chat.id
#     if id_user not in list_user_id:
#         list_user_id.append(id_user)
#         TelegramUserModel.objects.create(
#             user_id=id_user,
#             username=message.chat.username,
#             first_name=message.chat.first_name,
#         )

#     keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard.keyboard = main_menu
#     client.send_message(chat_id=message.chat.id,
#                         text=text,
#                         reply_markup=keyboard)


# @client.message_handler(func=lambda message: message.text.split()[0] == '♻️')
# def trade_series(message):
#     device = message.text.split()[1]
#     main_menu_series = TradeInSeriesModel.objects.filter(name__icontains=device)
#     main_menu_series = [['📍 ' + buttons.name] for buttons in main_menu_series]
#     if not main_menu_series:
#         trade_main(message=message,
#                    text='Этот раздел еще закрыт')
#         return 1
#     main_menu_series.append(['⬅️Назад к Trade-in'])
#     keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard.keyboard = main_menu_series
#     client.send_message(chat_id=message.chat.id,
#                         text='Выберите серию',
#                         reply_markup=keyboard)
#     UserStepModel.objects.filter(
#         user__user_id=message.chat.id
#     ).delete()


# @client.message_handler(func=lambda message: message.text.split()[0] == '📍')
# def trade_first_step(message, text='Далее выберите из указанных вариантов'):
#     device = message.text.replace('📍 ', '')
#     UserStepModel.objects.create(
#         user=TelegramUserModel.objects.filter(user_id=message.chat.id)[0],
#         steps_ok='1',
#         cost=TradeInSeriesModel.objects.filter(name=device)[0].start_cost,
#         device=device
#     )
#     steps = TradeInStepModel.objects.filter(series__name=device).filter(step=1)[0]
#     steps = VariableFoeStepModel.objects.filter(step=steps.id)
#     keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard.keyboard = [['📌 ' + i.name] for i in steps]
#     client.send_message(chat_id=message.chat.id,
#                         text=text,
#                         reply_markup=keyboard)


# @client.message_handler(func=lambda message: message.text.split()[0] == '📌')
# def trade_again_step(message):
#     user_data = UserStepModel.objects.filter(
#         user__user_id=message.chat.id,
#     )
#     device = user_data[0].device
#     step = user_data[0].steps_ok
#     max_step = TradeInSeriesModel.objects.filter(
#         name=device
#     )[0].max_step
#     if int(max_step) != int(step):
#         variable = VariableFoeStepModel.objects.filter(
#             step__step=step,
#             name=message.text.replace('📌 ', '')
#         )
#         new_cost = user_data[0].cost + variable[0].increase - variable[0].decrease
#         step = str(int(step) + 1)
#         UserStepModel.objects.filter(
#             user__user_id=message.chat.id,
#         ).update(
#             steps_ok=step,
#             cost=new_cost,
#         )
#         nex = TradeInStepModel.objects.filter(
#             step=step,
#             series__name=device
#         )
#         name = nex[0].name
#         next = VariableFoeStepModel.objects.filter(
#             step=nex[0].id
#         )
#         keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
#         keyboard.keyboard = [['📌 ' + i.name] for i in next]
#         client.send_message(chat_id=message.chat.id,
#                             text=name,
#                             reply_markup=keyboard)

#     else:
#         variable = VariableFoeStepModel.objects.filter(
#             step__step=step,
#             name=message.text.replace('📌 ', '')
#         )
#         new_cost = user_data[0].cost + variable[0].increase - variable[0].decrease
#         UserStepModel.objects.filter(
#             user__user_id=message.chat.id,
#         ).update(
#             cost=new_cost,
#         )
#         text = f'Оценка завершена!\n' \
#                f'Стоимость {str(new_cost)}'
#         trade_main(message=message,
#                    text=text)


def get_trade_products():
    result = Product.objects.values('name').filter(
        sell=False,
        booking=False,
        moderation=True,
        state__state='Новое устройство, выдано по гарантии взамен неисправному устройству в авторизованном сервисном '
                     'центре (АСЦ) Apple. Абсолютно новое, не активированное. '
    )
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


trade_product = get_trade_products()


@client.message_handler(commands=['sale'])
@client.message_handler(func=lambda message: message.text == '💥Скидки💥')
def tradein_model(message):
    sale = get_sale(message)
    if sale == []:
        start_message(message, 'Ничего не найдено')
        return 0
    result = [['🔻 ' + x] for x in sorted(sale)]
    result.append(['⬅️Главное меню'])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = result
    client.send_message(chat_id=message.chat.id,
                        text='Вот все скидки',
                        reply_markup=keyboard_products,
                        parse_mode='HTML')


@client.message_handler(func=lambda message: message.text == 'Ремонт устройств')
def main_menu_repair(message, text='Выберите устройство'):
    
    try:
        UserChoiceModel.objects.filter(
            user_id=TelegramUserModel.objects.get(
                user_id=message.chat.id
            ).id
        ).delete()
    except EOFError as _:
        pass

    buttons = ButtonModel.objects.all()
    buttons = [['🔧 ' + i.name_button] for i in buttons]
    buttons.append(['⬅️Главное меню'])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = buttons
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard_products,
                        parse_mode='MarkdownV2')


@client.message_handler(func=lambda message: message.text.split()[0] == '🔧')
def service_repair(message):
    device = message.text.replace('🔧 ', '').split('|', 1)[0]
    id_user = TelegramUserModel.objects.get(
        user_id=message.chat.id
    ).id
    user_device = UserChoiceModel.objects.filter(
        user_id=id_user
    )
    if not user_device:
        user_query = TelegramUserModel.objects.get(
            user_id=message.chat.id,
        )
        UserChoiceModel.objects.create(
            user_id=user_query,
            cost=0,
            device=device
        )
        buttons = ServiceModels.objects.filter(
            series__name_button=message.text.replace('🔧 ', '')
        )
        buttons = [['Завершить и показать сумму ремонта']] + \
                  [['🔧 ' +
                    i.name +
                    ' | ' +
                    str(i.cost) +
                    'p'
                    ] for i in buttons]
        buttons.append(['⬅️Главное меню'])
        keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_products.keyboard = buttons
        client.send_message(chat_id=message.chat.id,
                            text='text',
                            reply_markup=keyboard_products)
        return 1

    else:
        user_cost = user_device[0].cost
        user_device = user_device[0].device
        up = ServiceModels.objects.filter(
            series__name_button=user_device,
            name=device
        )

        buttons = ButtonModel.objects.get(
            name_button=user_device
        )
        buttons = ServiceModels.objects.filter(
            series=buttons
        )
        id_user = TelegramUserModel.objects.get(
            user_id=message.chat.id
        )
        id_user = UserChoiceModel.objects.get(
            user_id=id_user
        )
        xx = UseService.objects.filter(
            user=id_user,
        )
        if message.text in [i.name_service for i in xx]:
            pass
        else:
            UseService.objects.create(
                user=id_user,
                name_service=message.text
            )
            UserChoiceModel.objects.update(
                device=user_device,
                cost=str(int(user_cost) + int(up[0].cost))
            )
        buttons = [['Завершить и показать сумму ремонта']] + \
                  [['🔧 ' +
                    i.name +
                    ' | ' +
                    str(i.cost) +
                    'p'
                    ] for i in buttons]
        buttons.append(['⬅️Главное меню'])
        keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_products.keyboard = buttons
        client.send_message(chat_id=message.chat.id,
                            text=f'{message.text.replace("🔧 ", "")}'
                                 f'\n\n'
                                 f'Услуга успешно добавлена',
                            reply_markup=keyboard_products)


@client.message_handler(func=lambda message: message.text == 'Завершить и показать сумму ремонта')
def service_repair_exit(message):
    services = UseService.objects.filter(
        user_id=UserChoiceModel.objects.filter(
            user_id=TelegramUserModel.objects.get(
                user_id=message.chat.id
            ).id
        )[0].id
    )
    cost = UserChoiceModel.objects.filter(
        user_id=TelegramUserModel.objects.get(
            user_id=message.chat.id
        ).id
    )[0].cost
    text = "".join([' -- ' + i.name_service.replace("🔧 ", "")
                    + '\n' for i in services])
    text = 'Выбранные услуги: \n' + text
    text = text + f'\nИтоговая стоимость:\n{str(cost)} рублей'

    start_message(
        message=message,
        text=text
    )


from trade_trade.models import Trade

text_trade = """
Помимо новых и б/у устройств у нас всегда в наличии техника после гарантийного обмена, в простонародье — обменка

Что такое обменка? 

— Обменка это устройство, которое было заменено, не отремонтировано, не восстановлено,\
 а именно заменено по гарантии на абсолютно новое. 

Откуда появляются такие телефоны?

— Рассмотрим ситуацию: у нас есть б/у iPhone 11 с нерабочим, например, микрофоном/камерой/динамиком и т.д. ,\
 т.е. гарантийной поломкой, мы относим его в авторизованный сервисный центр: iPort, Re:Store, Amos, B2X, \
 Secret Service или к любому другому официальному дилеру, который занимается гарантийный обслуживаем. \
 Сервисный центр принимает наше устройство, выявляет неисправность и выдает нам новое устройство — обменку.\
  Это абсолютно новое, не активированное устройство, с официальной гарантией Apple 1 год. Все устройства с \
  обмена — Ростест, поскольку заменяются по гарантии на территории РФ. 

— Какая гарантия на Обменки?

Такая же гарантия как и на новое устройство в коробке, 1 год. Информацию можно проверить на официальном\
 сайте Apple или позвонить в службу поддержки

Если у вас остались вопросы, вы можете задать их по телефону: +7 (932) 222-54-45
"""


@client.message_handler(func=lambda message: message.text == 'Устройства с обменки')
def trade_again_step(message):
    tr_products = [['🔁 ' + i.name_button] for i in
                   Trade.objects.all()]
    if not tr_products:
        start_message(message=message,
                      text='В разделе сейчас пусто')
        return 1
    tr_products.append(['⬅️Главное меню'])
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = tr_products
    client.send_message(chat_id=message.chat.id,
                        text='https://www.youtube.com/watch?v=ARM-ZnxJcYI',
                        disable_web_page_preview=False,
                        )

    client.send_message(chat_id=message.chat.id,
                        text=text_trade,
                        reply_markup=keyboard,
                        )


@client.message_handler(commands=['GetService'])
def admin_main_menu(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():

        text = 'Стат за сегодня: /static_today' \
               '\nСтат по регистрации: /stat_all_user' \
               '\nСтат по разделам: ...' \
               '\nСтат по продажам: ...' \
               '\n\nОтключить ростест: /ru_test_False' \
               '\nВключить ростест: /ru_test_True'
        client.send_message(chat_id=message.chat.id,
                            text=text,
                            )
    else:
        start_message(message)


@client.message_handler(commands=['static_today'])
def admin_hours_users(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():

        text = 'Текущие данные по часам\n'
        stat = StaticUserHourModel.objects.all()
        today_reg = datetime.date.today().strftime('%m/%d/%Y')
        stat_count = stat.filter(date_created=today_reg).count()
        text += 'Всего: ' + str(stat_count) + '\n\n'
        _time = int((datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%H')) + 1
        i = 0
        while i != _time:
            s = stat.filter(hour_created=i, date_created=today_reg).count()
            st = f'{i}:00  -- {s} чел.\n'
            text += st
            i += 1
        client.send_message(chat_id=message.chat.id,
                            text=text + '\n\n\n Вернуться в сервисное меню /GetService',
                            )
    else:
        start_message(message)


@client.message_handler(commands=['stat_all_user'])
def admin_hours_users(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():

        text = 'Кол-во зарегистрированных пользователей\n\n'
        today_reg = datetime.date.today().strftime('%m/%d/%Y')
        stat = UserModel.objects.all()
        stat_count = stat.count()
        text += 'Всего: ' + str(stat_count)

        today_reg = stat.filter(date_created=today_reg).count()
        text += '\nСегодня: ' + str(today_reg)

        client.send_message(chat_id=message.chat.id,
                            text=text + '\n\n\n Вернуться в сервисное меню /GetService',
                            )
    else:
        start_message(message)


@client.message_handler(commands=['ru_test_False'])
def set_re_test_false(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():
        from tune_admin.models import SetTelegramModel
        SetTelegramModel.objects.all().update(flag_test=False)
        client.send_message(chat_id=message.chat.id,
                            text='Групповая наценка на Ростест ВЫКЛЮЧЕНА')
    else:
        start_message(message)


@client.message_handler(commands=['ru_test_True'])
def set_re_test_false(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():
        from tune_admin.models import SetTelegramModel
        SetTelegramModel.objects.all().update(flag_test=True)
        client.send_message(chat_id=message.chat.id,
                            text='Групповая наценка на Ростест ВКЛЮЧЕНА')
    else:
        start_message(message)


@client.message_handler(commands=['server_restart'])
def admin_hours_users(message):
    if UserModel.objects.filter(user_id=str(message.chat.id), super_user=True).exists():
        res = os.system('sudo supervisorctl status gunicorn | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs kill -HUP')
        client.send_message(chat_id=message.chat.id,
                            text=f'Статус перезагрузки: {res}' + '\n\n\n Показать сервисное меню /GetService',
                            )
    else:
        start_message(message)


@client.message_handler(content_types=['text'])
def bitrix_client(message):
    if str(message.chat.id) != '572982939':
        if message.text.lower().split()[0] == 'забронировать|узнать' or \
                message.text.lower() == 'купить новое устройство':
            start_message(message, text='Пожалуйста дождитесь ответа менеджера,'
                                        ' он поможет Вам забронировать устройство или расскажет о нем более подробно 👩🏻‍💻')
        if message.text.lower() == 'связаться с менеджером':
            start_message(message, text='Пожалуйста дождитесь ответа менеджера,'
                                        ' он поможет Вам забронировать устройство или расскажет о нем более подробно 👩🏻‍💻')
        jsn = message.__dict__.get('json')
        ts = {'update_id': 287246100,
              'message': jsn}

        requests.post(URL_BITRIX, json=ts)


@client.message_handler(content_types=['voice'])
def voice(message):
    jsn = message.__dict__.get('json')
    exit_dict = {"update_id": 287246100, "message": jsn}
    requests.post(URL_BITRIX, json=exit_dict)


@client.message_handler(content_types=['video'])
def video(message):
    jsn = message.__dict__.get('json')
    exit_dict = {"update_id": 287246100, "message": jsn}
    requests.post(URL_BITRIX, json=exit_dict)


@client.message_handler(content_types=['photo'])
def photo(message):
    jsn = message.__dict__.get('json')
    exit_dict = {"update_id": 287246100, "message": jsn}
    requests.post(URL_BITRIX, json=exit_dict)


@csrf_exempt
def bot(request):
    try:
        if request.META['CONTENT_TYPE'] == 'application/json':

            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            us_id = str(update.message.chat.id) + str(
                (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%H'))
            list_uss = StaticUserHourModel.objects.all()
            list_uss = [str(i.user_id) for i in list_uss]

            if str(us_id) not in list_uss:
                StaticUserHourModel.objects.create(
                    user_id=str(us_id),
                    date_created=datetime.date.today().strftime('%m/%d/%Y'),
                    hour_created=str((datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%H')),
                    full_id=str(update.message.chat.username),
                )
                start_message(message=update.message,
                              text='У нас обновились товары!\nВы автоматически возвращены в главное меню')
            else:
                client.process_new_updates([update])
            list_user = UserModel.objects.all()
            list_user_id = [str(user_id.user_id) for user_id in list_user]

            message = update.message
            if str(message.chat.id) not in list_user_id:
                UserModel.objects.create(
                    user_id=str(message.chat.id),
                    date_created=datetime.date.today().strftime('%m/%d/%Y'),
                    name=message.chat.username,
                    first_name=message.chat.first_name,
                    last_name=message.chat.last_name
                )

            return HttpResponse(200)
    except EncodingWarning as _:
        return HttpResponse(200)

    return HttpResponse(200)
