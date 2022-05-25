import csv
import re
from pprint import pprint

from cost_models.startsvc import new_cvs_data



def get_csv():
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
    return iphone_list


series_iphone = '13promax,|' \
                '13pro,|' \
                '13mini,|' \
                '13,|' \
                '12promax,|' \
                '12pro,|' \
                '12mini,|' \
                '12,|' \
                '11promax,|' \
                '11pro,|' \
                '11,|' \
                'iphonexr,|' \
                'iphonese,'

series_ipad = 'ipadair2021wi-ficellular,|' \
              'ipadair2021wi-fi,|' \
              'ipad2021wi-ficellular,|' \
              'ipad2021wi-fi,|' \
              'ipadmini2021wi-ficellular,|' \
              'ipadmini2021wi-fi,|' \
              'ipadpro112021wi-ficellular,|' \
              'ipadpro112021wi-fi,|' \
              'ipadpro12.92021wi-fi,|' \
              'ipadpro12.92021wi-ficellular,|' \
              'ipadair2022wi-ficellular,|' \
              'ipadair2022wi-fi,|' \
              'ipad2022wi-ficellular,|' \
              'ipad2022wi-fi,|' \
              'ipadmini2022wi-ficellular,|' \
              'ipadmini2022wi-fi,|' \
              'ipadpro112022wi-ficellular,|' \
              'ipadpro112022wi-fi,|' \
              'ipadpro12.92022wi-fi,'

series_watch = 'series3,|' \
               'seriesse,|' \
               'series6,|' \
               'series7gps,|' \
               'series7,|' \
               'se,'
size_watch = '35|' \
             '36|' \
             '37|' \
             '38|' \
             '39|' \
             '40|' \
             '41|' \
             '42|' \
             '43|' \
             '44|' \
             '45|' \
             '46|' \
             '47'


def get_clear_list(products):
    series = []
    series_cost = []
    for product in products:

        if 'америка' in product['Title'].lower():
            product['region'] = 'америка'
        else:
            product['region'] = 'ростест'
            # continue
        if 'iphone' in product['Title'].lower():

            product_ = 'iphone'
            product_ser = re.findall(series_iphone, product['Title'].replace(' ', '').lower())
            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                product_ += product_ser[0]
            else:
                product_ += product_ser[0]
            memory = '64|128|256|512|1тб'
            memory = re.findall(memory, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

        # --------------------------------------------------

        if 'ipad' in product['Title'].lower():
            product_ = 'ipad'
            product_ser = re.findall(series_ipad, product['Title'].replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                ).replace('+', ''))

            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                product_ += product_ser[0]
            else:
                product_ += product_ser[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

        # --------------------------------------------------
        if 'watch' in product['Title'].lower():
            product_ = 'watch'

            product_ser = \
            re.findall(series_watch, product['Title'].replace(' ', '').lower().replace('(', '').replace(
                ')', ''
            ))
            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                product_ += product_ser[0]
            else:
                product_ += product_ser[0]
            memory = re.findall(size_watch, (product['Title'] + product['Editions']).replace(' ', '').lower())[0]
            product_ += memory
            product_ += product['region']
            if product_ not in series:
                series.append(product_)

    xxx = list(set(series))
    for i in xxx:
        tmp_cost = '0'
        if 'iphone' in i.lower():

            product_ser = re.findall(series_iphone, i.replace(' ', '').lower())
            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                series_tmp = product_ser[0]
            else:
                series_tmp = product_ser[0]
            memory = '64|128|256|512|1тб'
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

            product_ser = re.findall(series_ipad, i.replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                ))
            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                series_tmp = product_ser[0]
            else:
                series_tmp = product_ser[0]
            memory = '64|128|256|512'
            memory = re.findall(memory, i.replace(' ', '').lower())[0]
            for j in products:

                z = (j['Title'] + j['Editions']).replace(' ', '').lower().replace('(', '').replace(
                    ')', ''
                ).replace('+', '')
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

            product_ser = re.findall(series_watch, i.replace(' ', '').lower().replace('(', '').replace(
                ')', ''
            ))
            if '' in product_ser:
                while '' in product_ser:
                    product_ser.remove('')
                series_tmp = product_ser[0]
            else:
                series_tmp = product_ser[0]
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
    costs = get_clear_list([i for i in get_csv() if i['Price'] != '0'])
    my_csv = get_csv()
    xxx = []
    from tune_admin.models import SetTelegramModel
    ru_test_flag = SetTelegramModel.objects.all()[0].flag_test
#     if SetTelegramModel.objects.all()[0].flag_test == True:
#         ru_test_flag = True
    for i in costs:
        if i['device'] == 'iphone':
            if i['region'] != 'ростест':
                if i['series'] != '':
                    for cs in my_csv:
                        if i['device'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():
                            if i['series'] in cs['Title'].replace(' ', '').lower() and \
                                    i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                                    i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():
                                if i['region'] == 'ростест' and ru_test_flag:
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)
                                elif i['region'] == 'америка':
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)
        # --------------------------------------------
        if i['device'] == 'ipad':
                if i['region'] == 'ростест':
                    for cs in my_csv:
                        if i['device'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():
                            if i['series'] in cs['Title'].replace(' ', '').lower().replace('(', '').replace(
                                    ')', '').replace('+', '') and \
                                    i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                                    i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():

                                if i['region'] == 'ростест' and ru_test_flag:
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)
                                elif i['region'] == 'америка':
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)

        # --------------------------------------------
        if i['device'] == 'watch':
                if i['region'] == 'ростест':
                    for cs in my_csv:
                        if i['device'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():
                            if i['series'] in cs['Title'].replace(' ', '').lower().replace('(', '').replace(
                                    ')', '') and \
                                    i['memory'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower() and \
                                    i['region'] in (cs['Title'] + cs['Editions']).replace(' ', '').lower():

                                if i['region'] == 'ростест' and ru_test_flag:
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)
                                elif i['region'] == 'америка':
                                    if cs['Price'] == '0':
                                        cs['Price'] = i['cost']
                                    if cs['Price'] != '0':
                                        xxx.append(cs)



    new_cvs_data(xxx)
