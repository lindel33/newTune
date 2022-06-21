import csv

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
import re

color = "красный|зеленый"


class TopicalCost:
    def __init__(self):
        self.iphone = []
        self.ipad = []
        self.airpods = []
        self.watch = []
        self.macbook = []

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
                if 'ipad' in i:
                    device = self._get_only_ipad(i)
                    self.ipad.append(device)
                if 'watch' in i:
                    device = self._get_only_watch(i)
                    self.watch.append(device)
                if 'airpods' in i:
                    device = self._get_only_airpods(i)
                    self.airpods.append(device)

                if 'macbook' in i:
                    device = self._get_only_macbook(i)
                    self.macbook.append(device)

    @staticmethod
    def _get_clear_line(lines):
        line = lines['Title'].lower()
        line = line.replace(' ', '')

        if 'macbook' not in line:
            line = line.replace('гб', '')
            line = line.replace('gb', '')
            line = line.replace('tb', '')
            line = line.replace('тб', '')

        line = line.replace('mm', '')

        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('-', '')
        line = line.replace('+', '')
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

            if 'iphonexr' in ser:
                ser = ser.replace('iphonexr', '')
                ser = ser + ' XR'
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
            'region': re.findall('америка|ростест', line)[0],
            'year': None,
        }

        return data

    @staticmethod
    def _get_only_ipad(line):
        global color
        from cost_models.service import colors
        save_line = line

        def get_series(ser, _year):

            if 'air' in ser:
                new_ser = 'Air ' + _year
                if 'cell' in ser:
                    return new_ser + ' Wifi + Cellular'
                else:
                    return new_ser + ' Wifi'
            if 'pro' in ser:
                new_ser = 'Pro ' + _year
                if '11' in ser:
                    new_ser += ' 11'
                elif '12' in ser:
                    new_ser += ' 12.9'
                if 'cell' in ser:
                    return new_ser + ' Wifi + Cellular'
                else:
                    return new_ser + ' Wifi'
            if 'mini' in ser:
                new_ser = 'Mini ' + _year
                if 'cell' in ser:
                    return new_ser + ' Wifi + Cellular'
                else:
                    return new_ser + ' Wifi'
            return 'Нет'

        series = 'ipadair2021wificellular,|' \
                 'ipadair2021wifi,|' \
                 'ipad2021wificellular,|' \
                 'ipad2021wifi,|' \
                 'ipadmini2021wificellular,|' \
                 'ipadmini2021wifi,|' \
                 'ipadpro112021wificellular,|' \
                 'ipadpro112021wifi,|' \
                 'ipadpro12.92021wifi,|' \
                 'ipadpro12.92021wificellular,|' \
                 'ipadair2022wificellular,|' \
                 'ipadair2022wifi,|' \
                 'ipad2022wificellular,|' \
                 'ipad2022wifi,|' \
                 'ipadmini2022wificellular,|' \
                 'ipadmini2022wifi,|' \
                 'ipadpro112022wificellular,|' \
                 'ipadpro112022wifi,|' \
                 'ipadpro12.92022wifi,'

        memory = '32,|64,|128,|256,|512,|1,|1024,'
        year = '2019|2020|2021|2022|2023|2023'
        year = re.findall(year, line)[0]
        series = get_series(re.findall(series, line)[0], year)
        color = re.findall(colors, line)[0]

        if memory == '1,':
            memory = '1 ТБ'
        if series == 'Нет':
            series = year
        else:
            series = series
        line = line.replace(series, '')

        memory = re.findall(memory, line)[0]

        data = {
            'device': 'iPad',
            'series': series.replace(',', ''),
            'memory': memory.replace(',', ''),
            'color': color,
            'cost': re.findall('\[(.*?)\]', line)[0],
            'extra': save_line,
            'region': re.findall('америка|ростест', line)[0],
            'year': year,
        }
        return data

    @staticmethod
    def _get_only_watch(line):
        global color
        from cost_models.service import colors
        save_line = line

        def get_series(sers, size):
            if 'series3' in sers:
                return 'Series 3 ' + size + ' мм'
            if 'series4' in sers:
                return 'Series 4 ' + size + ' мм'
            elif 'series5' in sers:
                return 'Series 5 ' + size + ' мм'
            elif 'series6' in sers:
                return 'Series 6 ' + size + ' мм'
            elif 'series7' in sers:
                return 'Series 7 ' + size + ' мм'
            elif 'series8' in sers:
                return 'Series 8 ' + size + ' мм'
            elif 'se' in sers:
                return 'Series SE ' + size + ' мм'

        memory = re.findall(size_watch, line)[0]
        series = re.findall(series_watch, line)[0]
        series = get_series(series, memory)

        color = re.findall(colors, line)[0]

        line = line.replace(series, '')

        data = {
            'device': 'Watch',
            'series': series.replace(',', ''),
            'memory': memory.replace(',', ''),
            'color': color,
            'cost': re.findall('\[(.*?)\]', line)[0],
            'extra': save_line,
            'region': re.findall('америка|ростест', line)[0],
        }
        return data

    @staticmethod
    def _get_only_airpods(line):
        global color
        from cost_models.service import colors
        save_line = line

        def get_series(ser):
            return ser

        memory = re.findall('2|3|max|pro', line)[0]
        mem_tmp = memory
        color = re.findall(colors, line)[0]

        if memory in ['2', '3', 'pro']:
            memory = '2/3/Pro'
        if memory == 'max':
            memory = 'Max'

        line = line.replace(memory, '')

        data = {
            'device': 'AirPods',
            'series': 'AirPods',
            'memory': memory,
            'mem_tmp': mem_tmp,
            'color': color,
            'cost': re.findall('\[(.*?)\]', line)[0],
            'extra': save_line,
            'region': re.findall('америка|ростест', line)[0],
        }

        return data

    @staticmethod
    def _get_only_macbook(line):
        global color
        from cost_models.service import colors
        save_line = line
        line = line.replace('gb', 'Гб', )
        year = '2019|2020|2021|2022|2023|2023'
        year = re.findall(year, line)[0]
        line = line.replace(year, '')

        def get_ssd(line_ssd):
            ssd = 'ssd128|ssd256|ssd512|ssd1024'
            ssd = re.findall(ssd, line_ssd)[0]
            ssd = ssd.replace('ssd', 'SSD ')
            return ssd

        def get_ram(line_ram):
            ssd = '8Гб|12Гб|16Гб|24Гб|32Гб'
            ssd = re.findall(ssd, line_ram)[0]
            return ssd

        def get_series(line_series):
            series = 'air13|pro13'
            series = re.findall(series, line_series)[0]
            series = series.replace('air', 'Air ')
            series = series.replace('pro', 'Pro ')
            return series

        color = re.findall(colors, line)[0]
        data = {
            'device': 'MacBook',
            'year': year,
            'series': get_series(line),
            'memory': get_ram(line),
            'memory_ssd': get_ssd(line),
            'color': color,
            'cost': re.findall('\[(.*?)\]', line)[-1],
            'region': re.findall('америка|ростест', line)[0],
            'extra': save_line,

        }
        return data
