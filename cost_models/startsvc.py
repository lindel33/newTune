# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from pprint import pprint


def get_cvs():
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
    return data


def get_cvs_data():
    iphone_list = []

    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            parent_uid = row.get('Parent UID')
            title = row.get('Title')
            editions = row.get('Editions')

            if parent_uid != '':
                if editions != '':
                    if title != '':
                        iphone_list.append({'Title': row['Title'],
                                            'Editions': row['Editions'],
                                            'Tilda UID': row['Tilda UID'],
                                            'Parent UID': row['Parent UID'],
                                            'Price': row['Price'], })
    ex = []
    for i in iphone_list:
        c = 0
        col_1 = i['Title']
        col_2 = i['Editions']
        for j in colors_list:
            if j in col_1:
                color_eng = colors_dict[j]
                i['Title'] = i['Title'].replace(j, color_eng)
                break

        for j in colors_list:
            if j in col_2:
                color_eng = colors_dict[j]
                i['Editions'] = i['Editions'].replace(j, color_eng)
                ex.append(i)
                break
    print('Начальная длина файла --> ', len(ex))
    return ex


def post_cvs(data_new):
    with open('/home/apple/code/project1/tune/cost_models/store1.csv', 'w', encoding='utf-8') as f:
        data = csv.DictWriter(f, fieldnames=aa, delimiter=';')
        data.writeheader()
        data.writerows(data_new)


def post_cvs1(data_new):
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'w', encoding='utf-8') as f:
        data = csv.DictWriter(f, fieldnames=v_2, delimiter=';')
        data.writeheader()
        data.writerows(data_new)


def get_ff():
    return open('/home/apple/code/project1/tune/cost_models/store1.csv', '+')


def get_cvs_data1():
    iphone_list = []
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            iphone_list.append(row)
    return iphone_list


def new_cvs_data(new_dict):
    list_cvs = get_cvs_data1()
    c = 0
    z = 0
    # print('Длина к записи', len(new_dict))
    for i in list_cvs:
        for j in new_dict:
            if i['Tilda UID'] == j['Parent UID']:
                i['Price'] = j['Price']
                i['date_created'] = datetime.today()
                i['Quantity'] = 123
                # list_cvs.remove(i)
                # list_cvs.append(j)
                c += 1
                break
            if i['Parent UID'] == j['Parent UID']:
                z += 1
                i['Price'] = j['Price']
                i['date_created'] = datetime.today()
                i['Quantity'] = 123
                break
    # for i in list_cvs:
    #     if i['Quantity'] == 1233333555:
    #         print(i['Title'])
    # print('Иттреаций: ', c, z)

    # print(len(list_cvs))
    post_cvs1(list_cvs)


colors_list = ['Сияющая звезда', 'Синий', 'Тёмная ночь', 'Чёрный', 'Небесно-голубой',
               'Серебристый', 'Золотой', 'Красный', 'Серый космос', 'Розовое золото',
               'Зелёный', 'Голубое небо', 'Белый', 'Желтый', 'Фиолетовый',
               'Графитовый', 'Темно-синий', 'Розовый песок', 'Коралловый', 'Сияющая звезда',
               'Тихоокеанский синий', '(PRODUCT)RED', 'Голубой', 'Розовый',
               'Зеленый', 'Черный', 'Темная ночь']

colors_dict = {'Синий': 'Blue',
               'Розовый': 'Pink',
               'Тёмная ночь': 'Black',
               'Чёрный': 'Black',
               'Небесно-голубой': 'Sky Blue',
               'Серебристый': 'Silver',
               'Золотой': 'Gold',
               'Красный': 'Red',
               'Серый космос': 'Space Gray',
               'Розовое золото': 'Rose Gold',
               'Зелёный': 'Green',
               'Голубое небо': 'Blue',
               'Белый': 'White',
               'Желтый': 'Yellow',
               'Фиолетовый': 'Purple',
               'Графитовый': 'Graphite',
               'Тёмно-синий': 'Midnight',  # Midnight
               'Розовый песок': 'Pink',  # 'Pink Sand'
               'Коралловый': 'Coral',
               'Сияющая звезда': 'Starlight',  # Starlight
               'Тихоокеанский синий': 'Pacific Blue',
               '(PRODUCT)RED': 'Red',
               'Голубой': 'Blue',
               'Зеленый': 'Green',
               'Черный': 'Black',
               'Темная ночь': 'Black',  # Dark Night
               'Темно-синий': 'Midnight', }


def new_color(title):
    new_title = ''
    for color in colors_list:

        if color in title:
            color_eng = colors_dict[color]

            new_title = title.replace(color, color_eng)
            # print(color, '--> ', color_eng, '-->  ', title, '--> ', new_title)

            return new_title

    raise 'colorError'


aa = ['Price Old',
      'Brand',
      'Category',
      'Characteristics:Bluetooth',
      'Characteristics:Full HD',
      'Characteristics:Активное шумоподавление',
      'Characteristics:Вес наушника',
      'Characteristics:Вид',
      'Characteristics:Время работы',
      'Characteristics:Встроенные динамики',
      'Characteristics:Голосовой набор',
      'Characteristics:Диагональ',
      'Characteristics:Звук',
      'Characteristics:Класс водонепроницаемости',
      'Characteristics:Количество SIM-карт',
      'Characteristics:Количество Thunderbolt 3 (USB-C)',
      'Characteristics:Количество USB 3.0',
      'Characteristics:Количество микрофонов',
      'Characteristics:Количество ядер',
      'Characteristics:Комплект поставки',
      'Characteristics:Макс. время работы',
      'Characteristics:Материал',
      'Characteristics:Материал корпуса',
      'Characteristics:Материал ремешка',
      'Characteristics:Модель',
      'Characteristics:Объем видеопамяти',
      'Characteristics:Операционная система',
      'Characteristics:Особенности',
      'Characteristics:Ответить/закончить разговор',
      'Characteristics:Процессор',
      'Characteristics:Размер изображения',
      'Characteristics:Разрешение',
      'Characteristics:Системные требования',
      'Characteristics:Соотношение сторон',
      'Characteristics:Спецификации',
      'Characteristics:Технология дисплея',
      'Characteristics:Тип',
      'Characteristics:Тип дисплея',
      'Characteristics:Тип корпуса',
      'Characteristics:Тип экрана',
      'Characteristics:Тыловая камера',
      'Characteristics:Частота',
      'Characteristics:Число пикселей на дюйм',
      'Characteristics:Число пикселей на дюйм (PPI)',
      'Characteristics:Экран',
      'Characteristics:Яркость',
      'Description',
      'Editions',
      'External ID', 'Height',
      'Length',
      'Mark',
      'Modifications',
      'Parent UID',
      'Photo',
      'Price',
      'Quantity',
      'SKU',
      'Text',
      'Tilda UID',
      'Title',
      'Weight',
      'Width',
      'date_created',]

v_2 = [
    "Tilda UID",
    'Brand',
    'SKU',
    'Mark',
    'Category',
    'Title',
    'Description',
    'Text',
    'Photo',
    'Price',
    'Quantity',
    "Price Old",
    'Editions',
    'Modifications',
    "External ID",
    "Parent UID",
    "Characteristics:Модель",
    "Characteristics:Операционная система",
    "Characteristics:Материал корпуса",
    "Characteristics:Количество SIM-карт",
    "Characteristics:Тип экрана",
    'Characteristics:Диагональ',
    "Characteristics:Размер изображения",
    "Characteristics:Число пикселей на дюйм (PPI)",
    "Characteristics:Соотношение сторон",
    "Characteristics:Тыловая камера",
    "Characteristics:Тип корпуса",
    'Characteristics:Тип дисплея',
    "Characteristics:Яркость",
    'Characteristics:Звук',
    'Characteristics:Макс. время работы',
    'Characteristics:Класс водонепроницаемости',
    'Characteristics:Материал ремешка',
    'Characteristics:Вид',
    'Characteristics:Тип',
    'Characteristics:Количество микрофонов',
    'Characteristics:Вес наушника',
    'Characteristics:Голосовой набор',
    'Characteristics:Ответить/закончить разговор',
    'Characteristics:Время работы',
    'Characteristics:Материал',
    'Characteristics:Активное шумоподавление',
    'Characteristics:Особенности',
    'Characteristics:Комплект поставки',
    'Characteristics:Спецификации',
    'Characteristics:Системные требования',
    'Characteristics:Процессор',
    'Characteristics:Экран',
    'Characteristics:Разрешение',
    'Characteristics:Число пикселей на дюйм',
    'Characteristics:Bluetooth',
    'Characteristics:Встроенные динамики',
    'Characteristics:Технология дисплея',
    'Characteristics:Full HD',
    'Characteristics:Частота',
    'Characteristics:Количество ядер',
    'Characteristics:Объем видеопамяти',
    'Characteristics:Количество Thunderbolt 3 (USB-C)',
    'Characteristics:Количество USB 3.0',
    'Weight',
    'Length',
    'Width',
    'Height',
    'date_created',

]

