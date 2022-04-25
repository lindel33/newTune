import time
import requests
import telebot
from data import (get_category, get_products,
                  get_detail_product, get_series,
                  get_current_product, get_not_category, filter_price, get_actual_price)

# TELEGRAM_URL = 'https://api.telegram.org/bot5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
TOKEN = '5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/cde3fe41e972cc1f1501bbd0a6d330a11644378495/'

client = telebot.TeleBot(TOKEN)
name_category = ['iPhone', 'iPad', 'MacBook',
                 'AirPods', 'Watch',
                 'Доп. устройства'] + get_not_category()

# client.set_webhook(url='https://tuneapple.pythonanywhere.com/api')
global_price = [
        ['От 0 до 10000'],
        ['От 10000 до 20000'],
        ['От 20000 до 30000'],
        ['От 30000 до 40000'],
        ['От 40000 до 50000'],
        ['От 50000 до 100000'],
        ['Главное меню'],
    ]
global_prices = [
        ['🙋Купить сейчас'],
        ['Прайс iPhone'],
        ['Прайс iPad'],
        ['Прайс MacBook'],
        ['Прайс Apple Watch'],
        ['Прайс AirPods'],
        ['Главное меню'],
    ]
current_category = list(set([x[1] for x in get_current_product()]))


@client.message_handler(regexp='Главное меню')
@client.message_handler(commands=['start'])
def start_message(message, text='Что хотите найти?'):
    category = get_category()
    categories = [[x[1]] for x in category]
    categories.insert(0, ['Мой бюджет'])
    categories.insert(1, ['Купить новое устройство'])

    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = categories
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard_category)


@client.message_handler(func=lambda message: message.text == 'Назад к прайсам')
@client.message_handler(func=lambda message: message.text == 'Купить новое устройство')
def actual_price(message):
    keyboard_actual = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_actual.keyboard = global_prices
    client.send_message(chat_id=message.chat.id,
                        text="Выберите раздел",
                        reply_markup=keyboard_actual)


@client.message_handler(func=lambda message: message.text.split()[0] == 'Прайс')
def price(message):
    text = get_actual_price(message.text)
    price_tmp = global_prices

    keyboard_actual = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_actual.keyboard = global_prices
    client.send_message(chat_id=message.chat.id,
                        text=text[0][1],
                        reply_markup=keyboard_actual)


@client.message_handler(func=lambda message: message.text
                                             in [x[1].split()[0] + ' ' + x[1].split()[1]
                                                 for x in get_products(message.text)])
def models(message):
    """
    Показывает все модели выбраного товара
    :param message:
    :return:
    """
    text = message.text
    products = [x[1] for x in get_products(text)]
    products.sort()
    products = [[x] for x in products]
    products.append(['Назад к ' + text.split()[0]])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = products
    client.send_message(chat_id=message.chat.id,
                        text='Ищу: ' + text,
                        reply_markup=keyboard_products)


@client.message_handler(func=lambda message: message.text == '📱 iPhone')
@client.message_handler(func=lambda message: message.text == 'Назад к iPhone')
def iphone_menu(message):
    text = 'iPhone'
    category = [[x[0]] for x in get_series(text) if x[0] in current_category]
    if category == []:
        start_message(message,
                          text='  '
                              ''
                              ' категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == '📲 iPad')
@client.message_handler(func=lambda message: message.text == 'Назад к iPad')
def ipad_menu(message):
    text = 'iPad'
    category = [[x[0]] for x in get_series(text) if x[0] in current_category]
    if category == []:
        start_message(message,
                      text='В этой категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == '💻 MacBook')
@client.message_handler(func=lambda message: message.text == 'Назад к MacBook')
def macbook_menu(message):
    text = 'MacBook'
    category = [[x[0]] for x in get_series(text) if x[0] in current_category]
    if category == []:
        start_message(message,
                      text='В этой категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == '🎧 AirPods')
@client.message_handler(func=lambda message: message.text == 'Назад к AirPods')
def airpods_menu(message):
    text = 'AirPods'
    category = [[x[0]] for x in get_series(text) if x[0] in current_category]
    if category == []:
        start_message(message,
                      text='В этой категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == '⌚️ Watch')
@client.message_handler(func=lambda message: message.text == 'Назад к Watch')
def watch_menu(message):
    text = 'Watch'
    category = [[x[0]] for x in get_series(text) if x[0] in current_category]
    if category == []:
        start_message(message,
                      text='В этой категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == '⌨️ Доп. устройства')
@client.message_handler(func=lambda message: message.text == 'Назад к Доп. устройствам')
def extra_menu(message):
    text = 'Доп. устройства'
    category = [[x[1]] for x in get_products(text)]
    if category == []:
        start_message(message,
                      text='В этой категори сейчас пусто😔\n'
                          'Следите за обнавлениями в канале\n'
                          ' https://t.me/tuneapple 👈')
        return 0
    category.append(['Главное меню'])
    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = category
    client.send_message(chat_id=message.chat.id,
                        text='Вот категории в наличие',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text == 'Мой бюджет')
@client.message_handler(func=lambda message: message.text == 'Расчитать еще раз')
def watch_menu(message):

    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = global_price
    client.send_message(chat_id=message.chat.id,
                        text='Выбор бюджета',
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text.split()[0] == 'От')
def cost_menu(message):
    text = message.text.split()
    price_min = text[1]
    price_max = text[3]
    price = [x[0] + '\n' for x in filter_price(price_min, price_max)]
    if price == []:
        keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_models_iphone.keyboard = global_price
        client.send_message(chat_id=message.chat.id,
                            text="Не найдено товаров",
                            reply_markup=keyboard_models_iphone)
        return 0
    price.sort(reverse=True)

    keyboard_price = [['Расчитать еще раз'],
                      ['Главное меню']] +\
                     [[x[0]] for x in filter_price(price_min, price_max)]

    keyboard_models_iphone = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_models_iphone.keyboard = keyboard_price
    client.send_message(chat_id=message.chat.id,
                        text="".join(price),
                        reply_markup=keyboard_models_iphone)


@client.message_handler(func=lambda message: message.text.split()[0] in name_category)
def send_message(message):
    print(message.chat.id)
    """
        Отправить сообщение
        :param message:
        :return:
    """
    name = message.text.split()
    name = name[0] + ' ' + name[1]
    products = [x[1] for x in get_products(name)]
    if message.text in products:
        products.remove(message.text)
    products.sort()
    products = [[x] for x in products]
    products.append(['🙋‍♀Забронировать\n' + message.text])

    if message.text.split()[0] not in get_not_category():
        products.append(['Назад к ' + message.text.split()[0]])
    else:
        products.append(['Назад к Доп. устройствам'])

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = products
    detail_product = get_detail_product(message.text)
    f1, f2, f3 = open('media/' + detail_product[1], 'rb'), \
                 open('media/' + detail_product[2], 'rb'), \
                 open('media/' + detail_product[3], 'rb')
    f1, f2, f3 = f1.read(), f2.read(), f3.read()

    client.send_media_group(chat_id=message.chat.id, media=[
        telebot.types.InputMediaPhoto(f1, caption=detail_product[6]),
        telebot.types.InputMediaPhoto(f2),
        telebot.types.InputMediaPhoto(f3), ])
    client.send_message(chat_id=message.chat.id,
                        text='Хотите забронировать эту модель?',
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text == '🙋Купить сейчас')
@client.message_handler(func=lambda message: message.text.split()[0] == '🙋‍♀Забронировать')
@client.message_handler(content_types=['text'])
def bitrix_message(message):
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
        if message.text.lower().split()[0] == '🙋‍♀забронировать' or \
                message.text.lower() == 'купить новое устройство' or \
                message.text.lower() == '🙋купить сейчас' or \
                message.text.lower() == 'как купить':
            start_message(message, text='Ваш запрос получен 👍 \n'
                                        'Менеджер уже в пути 🐌')
    except Exception as _:
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

client.polling(none_stop=True)
