import re
from pprint import pprint
from django.db import models
from price.models import Global, Iphone, Markup, Ipad
from .service import get_product_list
from .startsvc import get_cvs_data, new_cvs_data

mega_count = []
wifi_tmp = None

class ProviderModel(models.Model):
    name = models.CharField('Имя', max_length=20)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщик'

    def __str__(self):
        return self.name


class DetailModel(models.Model):
    device = models.CharField('Устройство', max_length=30)
    series = models.CharField('Серия', max_length=30)
    memory = models.CharField('Память', max_length=30)
    cost = models.CharField('Цена', max_length=30)
    color = models.CharField('Цвет', max_length=30)
    region = models.CharField('Регион', max_length=30)
    extra = models.CharField('Исходная строка', max_length=255)
    new_line = models.CharField('Строка состояния', max_length=255)
    provider = models.CharField('Поставщик', max_length=25)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Цены | Поиск'
        verbose_name_plural = 'Цены | Поиск'

    def __str__(self):
        return self.device


class NewPriceModel(models.Model):
    provider = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name='Поставщик')
    price = models.TextField('Новый прайс')
    id_products = []
    new_products = []
    csv_file = get_cvs_data()
    csv_file_copy = csv_file.copy()

    class Meta:
        verbose_name = 'Новый прайс | Управление cvs файлом'
        verbose_name_plural = 'Новый прайс | Управление cvs файлом'

    def __str__(self):
        return self.provider.name

    def save(self, *args, **kwargs):
        # self.csv_file = get_cvs_data()
        # self.id_products = []
        self.new_products = []
        list_new_products = get_product_list(self.price)

        zzz = 0
        for product in list_new_products:
            if product['region'].lower() == 'ростест':
                reg_tmp = '🇷🇺'
            else:
                reg_tmp = '🇺🇸'

            if product['memory'] == '1':
                mem_tmp = '1024'
            else:
                mem_tmp = product['memory']
            DetailModel.objects.create(
                device=product['device'],
                series=product['series'],
                memory=mem_tmp,
                cost=product['cost'],
                color=product['color'],
                region=reg_tmp,
                extra=product['extra'],
                provider=self.provider.name,
                new_line=str(product['device']) + ' ' +
                         str(product['series']) + ' ' +
                         str(product['memory']) + ' ' +
                         str(product['color']) + ' ' +
                         str(product['region']) + ' ' +
                         str(product['cost'])
            )
            next_product = self._get_csv_product(product)  # обновленные товары что есть в прайсе

            if next_product:
                self.new_products.append(next_product)
                zzz += 1

        new_cvs_data(self.new_products)
        super().save(*args, **kwargs)

    def set(self):
        self.set_new_price_on_grope(self.id_products)
        new_cvs_data(self.new_products)

        print('Запись')
    def _get_csv_product(self, product):
        """
        Поиск всех товаров в csv_file которые есть в свежем прайсе
        :param product:
        :return:
        """
        device = product['device'].lower()
        series = product['series'].lower()
        color = product['color'].lower()
        memory = self.get_memory(product['memory'].lower())
        memory_extra = '64|128|256|512'
        series = re.sub(memory_extra, '', series.lower())
        region = product['region'].lower()
        # series = self.get_series(series)
        series = series.replace(' ', '')
        if memory == '1':
            memory = 'тб'
        if region != 'ростест':
            region = ''
        for line in self.csv_file:
            title = line['Title'].lower().replace(' ', '')
            editions = line['Editions'].lower().replace(' ', '')
            if device in title or device in editions:
                if (series.replace(' ', '') + ',' in title.replace(' ', '') or
                    series.replace(' ', '') + ';' in editions.replace(' ', '')) \
                        and device != 'macbook':

                    if color in title or color in editions:
                        if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                            if region == 'ростест':

                                if region in title.replace(' ', '') or \
                                        region in editions.replace(' ', ''):
                                    self.csv_file.remove(line)
                                    new = self.new_cost(current_cost=line['Price'],
                                                        price_cost=product['cost'],
                                                        device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new
                                    id_pr = {
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region}
                                    self.id_products.append(id_pr)

                                    return line
                            else:
                                if 'рост' not in title.replace(' ', '') or \
                                        'рост' not in editions.replace(' ', ''):
                                    new = self.new_cost(current_cost=line['Price'],
                                                                  price_cost=product['cost'],
                                                                  device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new
                                    id_pr = {
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region}
                                    self.id_products.append(id_pr)

                                    return line
                elif device == 'macbook':
                    if (series.replace(' ', '') in title.replace(' ', '') or
                            series.replace(' ', '') in editions.replace(' ', '')):
                        if color in title or color in editions:

                            if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                                self.csv_file.remove(line)
                                new = self.new_cost(current_cost=line['Price'],
                                                    price_cost=product['cost'],
                                                    device=product['device'])
                                if float(line['Price']) < float(new):
                                    line['Price'] = new

                                self.id_products.append({
                                    'device': device,
                                    'series': series,
                                    'color': color,
                                    'memory': memory,
                                    'Tilda UID': line['Tilda UID'],
                                    'cost': line['Price'],
                                    'Title': line['Title'],
                                    'region': region,
                                    'ram_mac': product['ram_mac'].lower()})

                                return line

                elif device == 'ipad':
                    if (series.replace(' ', '') in title.replace(' ', '') or
                            series.replace(' ', '') in editions.replace(' ', '')):

                        if color in title or color in editions:
                            if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                                wifi = product['wifi'] + ','

                                if wifi in title.replace(' ', '') or wifi in editions.replace(' ', ''):
                                    if region == 'ростест':

                                        if region in title.replace(' ', '') or \
                                                region in editions.replace(' ', ''):
                                            self.csv_file.remove(line)
                                            new = self.new_cost(current_cost=line['Price'],
                                                                price_cost=product['cost'],
                                                                device=product['device'])
                                            if float(line['Price']) < float(new):
                                                line['Price'] = new

                                            self.id_products.append({
                                                'device': device,
                                                'series': series,
                                                'color': color,
                                                'memory': memory,
                                                'Tilda UID': line['Tilda UID'],
                                                'cost': line['Price'],
                                                'Title': line['Title'],
                                                'region': region,
                                                'wifi': product['wifi']})
                                            return line
                                    else:
                                        if 'рост' not in title.replace(' ', '') or \
                                                'рост' not in editions.replace(' ', ''):
                                            self.csv_file.remove(line)
                                            new = self.new_cost(current_cost=line['Price'],
                                                                price_cost=product['cost'],
                                                                device=product['device'])
                                            if float(line['Price']) < float(new):
                                                line['Price'] = new

                                            self.id_products.append({
                                                'device': device,
                                                'series': series,
                                                'color': color,
                                                'memory': memory,
                                                'Tilda UID': line['Tilda UID'],
                                                'cost': line['Price'],
                                                'Title': line['Title'],
                                                'region': region,
                                                'wifi': product['wifi']})
                                            return line

                elif device == 'watch':
                    if (series.replace(' ', '') in title.replace(' ', '') or
                            series.replace(' ', '') in editions.replace(' ', '')):
                        if color in title or color in editions:

                            if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                                if region == 'ростест':

                                    if region in title.replace(' ', '') or \
                                            region in editions.replace(' ', ''):
                                        self.csv_file.remove(line)
                                        new = self.new_cost(current_cost=line['Price'],
                                                            price_cost=product['cost'],
                                                            device=product['device'])
                                        if float(line['Price']) < float(new):
                                            line['Price'] = new

                                        self.id_products.append({
                                            'device': device,
                                            'series': series,
                                            'color': color,
                                            'memory': memory,
                                            'Tilda UID': line['Tilda UID'],
                                            'cost': line['Price'],
                                            'Title': line['Title'],
                                            'region': region})
                                        return line
                                else:
                                    if 'рост' not in title.replace(' ', '') or \
                                            'рост' not in editions.replace(' ', ''):
                                        self.csv_file.remove(line)
                                        new = self.new_cost(current_cost=line['Price'],
                                                            price_cost=product['cost'],
                                                            device=product['device'])
                                        if float(line['Price']) < float(new):
                                            line['Price'] = new

                                        self.id_products.append({
                                            'device': device,
                                            'series': series,
                                            'color': color,
                                            'memory': memory,
                                            'Tilda UID': line['Tilda UID'],
                                            'cost': line['Price'],
                                            'Title': line['Title'],
                                            'region': region})
                                        return line

                # -------------------> AirPods <-------------------

                elif device == 'airpods':
                    if (series.replace(' ', '') in title.replace(' ', '') or
                            series.replace(' ', '') in editions.replace(' ', '')):
                        if color and (color in title or color in editions):
                            if region == 'ростест':
                                if region in title.replace(' ', '') or \
                                        region in editions.replace(' ', ''):
                                    self.csv_file.remove(line)
                                    new = self.new_cost(current_cost=line['Price'],
                                                        price_cost=product['cost'],
                                                        device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new

                                    self.id_products.append({
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region})
                                    return line
                            else:
                                if 'рост' not in title.replace(' ', '') or \
                                        'рост' not in editions.replace(' ', ''):
                                    self.csv_file.remove(line)
                                    new = self.new_cost(current_cost=line['Price'],
                                                        price_cost=product['cost'],
                                                        device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new

                                    self.id_products.append({
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region})
                                    return line
                        elif color == 'Без цвета':
                            if region == 'ростест':
                                if region in title.replace(' ', '') or \
                                        region in editions.replace(' ', ''):
                                    self.csv_file.remove(line)
                                    new = self.new_cost(current_cost=line['Price'],
                                                        price_cost=product['cost'],
                                                        device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new

                                    self.id_products.append({
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region})
                                    return line
                            else:
                                if 'рост' not in title.replace(' ', '') or \
                                        'рост' not in editions.replace(' ', ''):
                                    self.csv_file.remove(line)
                                    new = self.new_cost(current_cost=line['Price'],
                                                        price_cost=product['cost'],
                                                        device=product['device'])
                                    if float(line['Price']) < float(new):
                                        line['Price'] = new

                                    self.id_products.append({
                                        'device': device,
                                        'series': series,
                                        'color': color,
                                        'memory': memory,
                                        'Tilda UID': line['Tilda UID'],
                                        'cost': line['Price'],
                                        'Title': line['Title'],
                                        'region': region})
                                    return line

    @staticmethod
    def new_cost(current_cost, price_cost, device) -> str:
        markup = Markup.objects.get(name_models=f'{device.replace(" ", "")}')
        if float(str(current_cost)) < float(str(price_cost)):
            if markup.flag:
                new_cost = float(price_cost) + (float(price_cost) * markup.markup / 100)
                exit_cost = [x for x in str(int(new_cost))]
                exit_cost[-3], exit_cost[-2], exit_cost[-1] = '9', '9', '0'
                return str(int("".join(exit_cost)))
            if not markup.flag:
                new_cost = str(int(float(price_cost)) + int(float(markup.markup_int)))
                exit_cost = [x for x in str(int(float(new_cost)))]
                exit_cost[-2], exit_cost[-1] = '9', '0'
                new_cost = str(int("".join(exit_cost)))
                return new_cost
        else:
            new_cost = str(int(float(price_cost)) + int(float(markup.markup_int)))
            exit_cost = [x for x in str(int(float(new_cost)))]
            exit_cost[-2], exit_cost[-1] = '9', '0'
            new_cost = str(int("".join(exit_cost)))
            return new_cost

    def set_new_price_on_grope(self, product_list):
        """
        Вернет товар который не найден в _get_csv_product по uid
        Для выставления цены на группу товаров
        Два пробега работает? :|
        :param product_list:
        :return:
        """
        global series_1, ram_mac
        global series_2
        wifi = None
        c = 0
        
        while c != 50:
            clear_list = self.get_clear_list(product_list)
            for product in clear_list:
                device = product['device'].lower()
                series = product['series'].lower()
                if 'ram_mac' in product:
                    ram_mac = product['ram_mac'].lower()
                if device == 'iphone':
                    series_1 = series.replace(' ', '') + ','
                    series_2 = series.replace(' ', '') + ';'
                if device == 'ipad':
                    global wifi_tmp

                    wifi = product['wifi'].lower()
                    if wifi == 'wi-fi':
                        wifi = 'wi-fi,'
                    series_1 = series.replace(' ', '')
                    series_2 = series.replace(' ', '')
                if device == 'watch':
                    series_1 = series.replace(' ', '') + ''
                    series_2 = series.replace(' ', '') + ''
                if device == 'macbook':
                    series_1 = series.replace(' ', '') + ''
                    series_2 = series.replace(' ', '') + ';'
                    ram_mac = ram_mac

                if device == 'airpods':
                    series_1 = series.replace(' ', '') + ''
                    series_2 = series.replace(' ', '') + ''

                color = product['color'].lower()
                memory = product['memory'].lower()
                if memory == '1':
                    memory = 'тб'
                for line in self.csv_file:
                    title = line['Title'].lower()
                    editions = line['Editions'].lower()
                    if line['Price'] == '0':
                        if device in title or device in editions:

                            if series_1 in title.replace(' ', '') or \
                                    series_2 in editions.replace(' ', ''):

                                if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):

                                    if wifi and device == 'ipad':

                                        if wifi in title.replace(' ', '') or \
                                                wifi in editions.replace(' ', ''):
                                            if product['region'] == 'ростест':
                                                if 'рост' in title.replace(' ', '') or \
                                                        'рост' in editions.replace(' ', ''):
                                                    if float(line['Price']) < float(product['cost']):
                                                        line['Price'] = product['cost']
                                                    self.new_products.append(line)

                                            else:
                                                if 'рост' not in title.replace(' ', '') or \
                                                        'рост' not in editions.replace(' ', ''):
                                                    # self.csv_file.remove(line)
                                                    if float(line['Price']) < float(product['cost']):
                                                        line['Price'] = product['cost']
                                                    self.new_products.append(line)
                                    elif device == 'macbook':

                                        if ram_mac in title.replace(' ', '') or \
                                                ram_mac in editions.replace(' ', ''):
                                            if product['region'] == 'ростест':
                                                if 'рост' in title.replace(' ', '') or \
                                                        'рост' in editions.replace(' ', ''):
                                                    if float(line['Price']) < float(product['cost']):
                                                        line['Price'] = product['cost']
                                                    self.new_products.append(line)

                                            else:
                                                if 'рост' not in title.replace(' ', '') or \
                                                        'рост' not in editions.replace(' ', ''):
                                                    # self.csv_file.remove(line)
                                                    if float(line['Price']) < float(product['cost']):
                                                        line['Price'] = product['cost']
                                                    self.new_products.append(line)

                                    elif not wifi or device != 'ipad':

                                        if product['region'] == 'ростест':
                                            if 'рост' in title.replace(' ', '') or \
                                                    'рост' in editions.replace(' ', ''):
                                                if float(line['Price']) < float(product['cost']):
                                                    line['Price'] = product['cost']
                                                self.new_products.append(line)

                                        else:
                                            if 'рост' not in title.replace(' ', '') or \
                                                    'рост' not in editions.replace(' ', ''):

                                                if float(line['Price']) < float(product['cost']):
                                                    # print(line['Price'], product['cost'])
                                                    line['Price'] = product['cost']
                                                self.new_products.append(line)

            c += 1

    def get_memory(self, memory):
        new_memory = memory.replace(' ', '')
        prefix_memory = 'гб|gb|тр|tb'
        #         if re.findall(prefix_memory, new_memory.lower()):
        new_memory = re.sub(prefix_memory, '', new_memory.lower())
        new_memory = new_memory.replace(' ', '')

        return new_memory

    def get_series(self, series):
        if len(series.split()) > 1:
            new_series = series.split()[1]
            return new_series
        if len(series.split()) == 1:
            new_series = series
            return new_series
        return 'Series not search'

    def get_clear_list(self, products):
        series = []
        series_cost = []
        for product in products:

            if product['region'] == 'америка':
                product['region'] = ''
            product['extra_series'] = product['series'] + product['memory'] + product['region']
            if product['extra_series'] not in series:
                series.append(product['extra_series'])
        xxx = list(set(series))

        for i in xxx:

            tmp_cost = '0'
            series_tmp = ''

            for j in products:
                if i == j['extra_series']:
                    series_tmp = j
                    products.remove(j)
                    if float(j['cost']) > float(tmp_cost):
                        tmp_cost = j['cost']

            series_tmp['cost'] = tmp_cost
            series_cost.append(series_tmp)
            xxx.remove(i)


        return series_cost

    def get_products_len(self, products):
        count = 0
        for product in products:
            device = product['device'].lower()
            series = product['series'].lower()
            memory = product['memory'].lower()
            if memory == '1':
                memory = 'тб'
            for line in self.csv_file:
                title = line['Title'].lower()
                editions = line['Editions'].lower()
                if device in title or device in editions:
                    if series.replace(' ', '') + ',' in title.replace(' ', '') or \
                            series.replace(' ', '') + ';' in editions.replace(' ', ''):

                        if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                            count += 1

        return count
