import csv
import requests


username = 'TuneApple'
token = 'd1cfd6bbfc894c3592932df061dd238d291fb5e3'
domain_name = 'TuneApple.pythonanywhere.com'
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


def get_cvs_data1():
    iphone_list = []
    with open('/home/apple/code/project1/tune/cost_models/store_clear.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            iphone_list.append(row)
    return iphone_list


def new_cvs_data():
    list_cvs = get_cvs_data1()

    for i in list_cvs:
        i['Price'] = '0'
    return list_cvs


def post_cvs1(data_new):
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'w', encoding='utf-8') as f:
        data = csv.DictWriter(f, fieldnames=v_2, delimiter=';')
        data.writeheader()
        data.writerows(data_new)


def restart_server():
    pass
#     response = requests.post(
#         'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
#             username=username,
#             domain_name=domain_name
#         ),
#         headers={'Authorization': 'Token {token}'.format(token=token)}
#     )
