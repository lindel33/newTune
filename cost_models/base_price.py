import csv

# series_ipad = 'ipadair2021wi-ficellular,|' \
#               'ipadair2021wi-fi,|' \
#               'ipad2021wi-ficellular,|' \
#               'ipad2021wi-fi,|' \
#               'ipadmini2021wi-ficellular,|' \
#               'ipadmini2021wi-fi,|' \
#               'ipadpro112021wi-ficellular,|' \
#               'ipadpro112021wi-fi,|' \
#               'ipadpro12.92021wi-fi,|' \
#               'ipadpro12.92021wi-ficellular,|' \
#               'ipadair2022wi-ficellular,|' \
#               'ipadair2022wi-fi,|' \
#               'ipad2022wi-ficellular,|' \
#               'ipad2022wi-fi,|' \
#               'ipadmini2022wi-ficellular,|' \
#               'ipadmini2022wi-fi,|' \
#               'ipadpro112022wi-ficellular,|' \
#               'ipadpro112022wi-fi,|' \
#               'ipadpro12.92022wi-fi,'
#
# series_watch = 'series3,|' \
#                'seriesse,|' \
#                'series6,|' \
#                'series7gps,|' \
#                'series7,|' \
#                'se,'
# size_watch = '35|' \
#              '36|' \
#              '37|' \
#              '38|' \
#              '39|' \
#              '40|' \
#              '41|' \
#              '42|' \
#              '43|' \
#              '44|' \
#              '45|' \
#              '46|' \
#              '47'
import re

color = "красный|зеленый"


class TopicalCost:
    def __init__(self):
        self.iphone = []

    @staticmethod
    def _get_csv_file():
        from cost_models.startsvc import get_cvs_data
        return get_cvs_data()

    def get_clear(self):
        for i in self._get_csv_file():
            i = self._get_clear_line(i)
            if '[0]' not in i and '[0.0]' not in i and '[]' not in i:
                if 'iphone' in i:
                    device = self._get_only_iphone(i)
                    self.iphone.append(device)

    @staticmethod
    def _get_clear_line(lines):
        line = lines['Title'].lower()
        line = line.replace(' ', '')

        line = line.replace('гб', '')
        line = line.replace('gb', '')
        line = line.replace('tb', '')
        line = line.replace('тб', '')
        line = line.replace('mm', '')
        line = line
        return line + f'[{lines["Price"]}]'

    @staticmethod
    def _get_only_iphone(line):
        global color
        from cost_models.service import colors

        def get_series(ser):
            if 'promax' in ser:
                ser = ser.replace('promax', '')
                ser = ser + ' Pro Max'
                return ser

            if 'pro' in ser:
                ser = ser.replace('pro', '')
                ser = ser + ' Pro'
                return ser

            if 'mini' in ser:
                ser = ser.replace('mini', '')
                ser = ser + ' Mini'
                return ser

            if 'iphonese' in ser:
                ser = ser.replace('iphonese', '')
                ser = ser + ' SE'
                return ser

            return ser

        series = '13promax,|13pro,|13mini,|13,|' \
                 '12promax,|12pro,|12mini,|12,|' \
                 '11promax,|11pro,|11,|' \
                 'iphonexr,|iphonese,'

        memory = '64,|128,|256,|512,|1,|1024,'
        series = get_series(re.findall(series, line)[0])
        line = line.replace(series, '')

        memory = re.findall(memory, line)[0]

        if memory == '1,':
            memory = '1 ТБ'
        color = re.findall(colors, line)[0]
        data = {
            'device': 'iPhone',
            'series': series.replace(',', ''),
            'memory': memory.replace(',', ''),
            'color': color,
            'cost': re.findall('\[(.*?)\]', line)[0],
            'extra': line,
            'region': re.findall('америка|ростест', line)[0]
        }

        return data
