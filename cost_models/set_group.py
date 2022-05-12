import csv
import re
from pprint import pprint

from cost_models.startsvc import new_cvs_data

colors = 'Голубой|' \
         'Синий|' \
         'Небесно-голубой|' \
         'Альпийский зеленый|' \
         'Зеленый|' \
         'Золотой'


def get_csv():
    iphone_list = []

    with open('/home/oem/projects/TuneApple/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
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
    return iphone_list


update = [i for i in get_csv() if i['Price'] != '0']

series_iphone = '13promax,|' \
                '13pro,|' \
                '13,|' \
                '12promsx,|' \
                '12pro,|' \
                '12'

series_ipad = 'ipadair2021wi-fi+cellular,|' \
              'ipadair2021wi-fi,|' \
              'ipad2021wi-fi+cellular,|' \
              'ipad2021wi-fi,|' \
              'ipadmini2021wi-fi+cellular,|' \
              'ipadmini2021wi-fi,'

series_watch = 'series3,|' \
               'seriesse,|' \
               'series6,|' \
               'series7gps,|' \
               'series7,'
size_watch = '35mm,|' \
             '36mm,|' \
             '37mm,|' \
             '38mm,|' \
             '39mm,|' \
             '40mm,|' \
             '41mm,|' \
             '42mm,|' \
             '43mm,|' \
             '44mm,|' \
             '45mm,|' \
             '46mm,|' \
             '47mm,'
def get_clear_list(products):
    series = []
    series_cost = []
    for product in products:

        if 'америка' in product['Title'].lower():
            product['region'] = 'америка'
        else:
            product['region'] = 'ростест'
        if 'iphone' in product['Title'].lower():
            product_ = 'iphone'
            product_ += re.findall(series_iphone, product['Title'].replace(' ', '').lower())[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

        # --------------------------------------------------
        if 'ipad' in product['Title'].lower():
            product_ = 'ipad'
            product_ += re.findall(series_ipad, product['Title'].replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                ))[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

        # --------------------------------------------------
        if 'watch' in product['Title'].lower():
            product_ = 'watch'
            product_ += \
            re.findall(series_watch, product['Title'].replace(' ', '').lower().replace('(', '').replace(
                ')', ''
            ))[0]
            memory = re.findall(size_watch, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

    xxx = list(set(series))
    for i in xxx:
        tmp_cost = '0'
        if 'iphone' in i.lower():

            series_tmp = re.findall(series_iphone, i.replace(' ', '').lower())[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, i.replace(' ', '').lower())[0]
            for j in products:
                z = (j['Title'] + j['Editions']).replace(' ', '').lower()
                if memory in z and series_tmp in z:
                    if float(j['Price']) > float(tmp_cost):
                        tmp_cost = j['Price']
            if 'ростест' in i:
                reg = 'ростест'
            if 'америка' in i:
                reg = 'америка'
            series_cost.append({
                'series': series_tmp,
                'cost': tmp_cost,
                'device': 'iphone',
                'memory': memory,
                'region': reg
            })
        # ----------------------------------------
        if 'ipad' in i.lower():

            series_tmp = re.findall(series_ipad, i.replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                ))[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, i.replace(' ', '').lower())[0]
            for j in products:

                z = (j['Title'] + j['Editions']).replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                )
                if memory in z and series_tmp in z:
                    if float(j['Price']) > float(tmp_cost):
                        tmp_cost = j['Price']
            if 'ростест' in i:
                reg = 'ростест'
            if 'америка' in i:
                reg = 'америка'
            series_cost.append({
                'series': series_tmp,
                'cost': tmp_cost,
                'device': 'ipad',
                'memory': memory,
                'region': reg
            })

        # ----------------------------------------
        if 'watch' in i.lower():

            series_tmp = re.findall(series_watch, i.replace(' ', '').lower().replace('(', '').replace(
                ')', ''
            ))[0]
            memory = re.findall(size_watch, i.replace(' ', '').lower())[0]
            for j in products:

                z = (j['Title'] + j['Editions']).replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                )

                if memory in z and series_tmp in z:
                    if float(j['Price']) > float(tmp_cost):
                        tmp_cost = j['Price']

            if 'ростест' in i:
                reg = 'ростест'
            if 'америка' in i:
                reg = 'америка'
            series_cost.append({
                'series': series_tmp,
                'cost': tmp_cost,
                'device': 'watch',
                'memory': memory,
                'region': reg
            })
    return series_cost


def set_group_cost():
    costs = get_clear_list(update)
    my_csv = get_csv()
    for i in costs:
        if i['device'] == 'iphone':

            for cs in my_csv:
                if i['series'] in cs['Title'].replace(' ', '').lower() and \
                        i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                        i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():

                    if cs['Price'] == '0':
                        cs['Price'] = i['cost']
        # --------------------------------------------
        if i['device'] == 'ipad':
            for cs in my_csv:

                if i['series'] in cs['Title'].replace(' ', '').lower().replace('(', '').replace(
                        ')', '') and \
                        i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                        i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():

                    if cs['Price'] == '0':
                        cs['Price'] = i['cost']

        # --------------------------------------------
        if i['device'] == 'watch':
            for cs in my_csv:

                if i['series'] in cs['Title'].replace(' ', '').lower().replace('(', '').replace(
                        ')', '') and \
                        i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                        i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():

                    if cs['Price'] == '0':
                        cs['Price'] = i['cost']

    new_cvs_data(my_csv)
    import time
    time.sleep(3)
