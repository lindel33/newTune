# -*- coding: utf-8 -*-
from pprint import pprint

from django.db import models
from .text_default import text_default
from .new_post import send_post
import datetime

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=4)
state_1 = 'Новое устройство, вскрыта упаковка. Не активировано.'
state_2 = 'Новое устройство, выдано по гарантии взамен неисправному устройству в авторизованном сервисном центре (АСЦ) Apple. Абсолютно новое, не активированное.'
state_3 = 'Устройство в идеальном состоянии. Полностью работоспособно. Не имеет царапин и потертостей на корпусе и дисплее.'
state_4 = 'Устройство в отличном состоянии. Полностью работоспособно. На корпусе и/ или дисплее минимальные царапины и потертости. Без проблем закроются премиум защитным стеклом/чехлом.'
state_5 = 'Устройство в хорошем состоянии. Полностью работоспособно. На корпусе и/ или дисплее есть царапины и потертости. Без проблем закроются премиум защитным стеклом/чехлом.'
states = [(state_1, 'Новый'),
          (state_2, 'Обменка'),
          (state_3, 'Как новый'),
          (state_4, 'Отличное'),
          (state_5, 'Хорошее ')
          ]

kit_1 ='Только устройство'
kit_2 = 'Коробка'
kit_3 = 'Коробка, кабель Lightning — USB-C для быстрой зарядки'
kit_4 = 'Кабель Lightning — USB-C для быстрой зарядки'
kit_5 = 'Коробка, кабель Lightning — USB для зарядки'
kit_6 = 'Только часы'
kit_7 = 'Часы + зарядное устройство '
kit_8 = 'Кабель USB‑C для быстрой зарядки Apple Watch '
kit_9 = 'Кабель USB для зарядки Apple Watch'
kit_full = 'Полный'
choices_kit = [
    ('Без комплекта', kit_1),
    (kit_2, kit_2),
    (kit_3, kit_3),
    (kit_4, kit_4),
    (kit_5, kit_5),
    (kit_6, kit_6),
    (kit_7, kit_7),
    (kit_8, kit_8),
    (kit_9, kit_9),
    (kit_full, kit_full),
]
choices_smile = [
    ('🔥', '🔥'),
    ('💥', '💥'),
    ('⚡', '⚡'),
    ('₽','₽')
]

guaranty_1 = 'Гарантия от магазина на проверку 3 месяца!✅'
guaranty_2 = 'Официальная гарантия Apple 2 года!✅'
guaranty_3 = 'Официальная гарантия Apple 1 год!✅'

choices_guaranty = [
    (guaranty_1, guaranty_1),
    (guaranty_2, guaranty_2),
    (guaranty_3, guaranty_3),
]


class KitModel(models.Model):
    kit = models.CharField('Текст', max_length=255)

    class Meta:
        verbose_name = 'Комплект'
        verbose_name_plural = 'Комплекты'

    def __str__(self):
        return self.kit


class GuarantyModel(models.Model):
    guaranty = models.CharField('Текст', max_length=255)
    guaranty_id = models.CharField('Текст', max_length=255)      
    class Meta:
        verbose_name = 'Гарантии'
        verbose_name_plural = 'Гарантии'

    def __str__(self):
        return self.guaranty


tests_1 = 'Ростест🇷🇺'
tests_2 = 'Не Ростест'
choices_tests = [
    (tests_1, tests_1),
    (tests_2, tests_2),
    ]
default_guaranty = 'Гарантия от магазина на проверку 3 месяца !✅'
default_text = text_default


def get_deadline():
    return datetime.datetime.today() + datetime.timedelta(days=5)


class Category(models.Model):
    category = models.CharField('Категория', max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.category)


class SeriesCategory(models.Model):
    category = models.CharField('Категория', max_length=100)

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'


    def __str__(self):
        return str(self.category)



class Product(models.Model):
    """
    Модель товара
    """

    image_1 = models.ImageField('Картинка 1',
                                upload_to='',
                                null=False,
                                )
    image_2 = models.ImageField('Картинка 2',
                                upload_to='',
                                null=False,
                                )
    image_3 = models.ImageField('Картинка 3',
                                upload_to='',
                                blank=True,
                                )
    sell = models.BooleanField('Продано?', default=False)
    booking = models.BooleanField('Забронированно?', default=False)
    moderation = models.BooleanField('Допущен к публикации?', default=True)
    price = models.PositiveIntegerField('Цена')

    smile = models.CharField('Эмодзи к цене', max_length=5, choices=choices_smile, null=True, blank=True,
                             help_text='Оставить пустым, если не нужен', default='₽')
    name = models.CharField('Название', max_length=150, null=False,
                            help_text='Пример: iPhone 7 128 Blue ||'
                                      'Формат: Модель/ Серия/ (Память/ Цвет/ Регион)-> если есть \n ' )
    name_tmp = models.CharField('Фоновое имя', max_length=100, null=False)
    tests = models.BooleanField('Ростест?', default=False)
    article = models.CharField('Код товара', max_length=15, null=False,
                               help_text='Пример: 20X100ZT')
    state = models.TextField('Состояние', choices=states, null=False,
                             help_text='Выбор сгенерирует шаблон')
    state_akb = models.SmallIntegerField('Состояние АКБ', default=0,
                                         help_text='Оставить в поле 0, если по АКБ нет информации')
    works = models.TextField('Произведенные работы', null=True, blank=True,
                             help_text='Оставить поле пустым, если не нужно')
    kit = models.ForeignKey(KitModel, on_delete=models.CASCADE, verbose_name='Комплект', null=True, blank=True, default=1)

    guaranty = models.ForeignKey(GuarantyModel, on_delete=models.CASCADE, verbose_name='Гарантия')
    custom_guaranty = models.DateField('Своя гарантия', null=True, blank=True)

    base_text = models.TextField('Нижняя подпись к посту', null=False, default=default_text)
    day_created = models.DateTimeField('Дата создания', auto_now_add=True)
    day_next_publish = models.DateTimeField('Дата следующего поста', default=get_deadline)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Модель', null=True, blank=True)
    series = models.ForeignKey(SeriesCategory, on_delete=models.CASCADE,
                               verbose_name='Серия', null=True, blank=True)

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, verbose_name='Автор',)
    count = models.SmallIntegerField('Счетчик сохранений', default=0)
    up_price = models.BooleanField('Цена поднята?', default=False)

    provider_device = models.CharField('Поставщик', max_length=50,default='Устройсво клиента', choices=[
                                                                                                    ('Устройсво клиента', 'Устройсво клиента'),
                                                                                                    ('Илья Савичев', 'Илья Савичев'),
                                                                                                    ('Эмиль', 'Эмиль'),
                                                                                                        ],
                                                                                                        )
    sale = models.BooleanField('Скидка', default=False)
    device_provider = models.BooleanField('Устройство поставщика', default=False)
    www = models.BooleanField('Первичное SMT', default=True)


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def save(self, extra=None, *args, **kwargs):

        if extra == '+':
            self.price += 1000
        if extra == '-':
            self.price -= 1000
        if extra == 'ВРЕМЕННО+':
            self.price += 4000
        if extra == 'ВРЕМЕННО-':
            self.price -= 4000

        if extra == 'Продажа':
            self.sell = True

        if extra == 'проц10':
            cost = self.price
            if len(str(cost)) >= 4:
                new_cost = (cost * 10 / 100) + cost
                exit_cost = [x for x in str(int(new_cost))]
                exit_cost[-3], exit_cost[-2], exit_cost[-1] = '9', '9', '0'
                self.price = int("".join(exit_cost))

        if extra == 'проц20':
            cost = self.price
            if len(str(cost)) >= 4:
                new_cost = (cost * 20 / 100) + cost
                exit_cost = [x for x in str(int(new_cost))]
                exit_cost[-3], exit_cost[-2], exit_cost[-1] = '9', '9', '0'
                self.price = int("".join(exit_cost))

        if extra == 'проц30':
            cost = self.price
            if len(str(cost)) >= 4:
                new_cost = (cost * 30 / 100) + cost
                exit_cost = [x for x in str(int(new_cost))]
                exit_cost[-3], exit_cost[-2], exit_cost[-1] = '9', '9', '0'
                self.price = int("".join(exit_cost))

        self.base_text = text_default
        price_list = []
        for element in str(self.price):
            price_list.append(element)
        last_1 = price_list.pop(-1)
        last_2 = price_list.pop(-1)
        last_3 = price_list.pop(-1)
        result_price = "".join(price_list) + '.' + last_3 + last_2 + last_1

        self.count = int(self.count) + 1

        if self.count == 1:
            self.name_tmp = str(self.name)

        if self.tests:
            self.name = str(self.name_tmp) + ' '+ 'Ростест🇷🇺'
        else:
            self.name = str(self.name_tmp)

        self.name = str(self.name)  + ' - ' + str(result_price)

        if self.smile:
            self.name = str(self.name) + str(self.smile)


        self.base_text = str(self.name) + '\n\n' + 'Код товара: ' + str(self.article) + '\n\n'\
                                 + str(self.state) + '\n'\

        self.base_text = str(self.base_text) + '\nКомплект: ' + str(self.kit) + '\n'

        if self.state_akb != 0:
            self.base_text = str(self.base_text) + '\nРодной аккумулятор: ' + str(self.state_akb) + '%\n'

        if self.works:
            self.base_text = str(self.base_text) + '\n' + str(self.works) + '\n'

        if not self.guaranty:
            castom_guarnt = datetime.datetime.strptime(str(self.custom_guaranty),'%Y-%m-%d').strftime('%d-%m-%Y')
            self.base_text = str(self.base_text) + '\nОфициальная гарантия Apple до '\
                             + str(castom_guarnt) + '\n'
        else:
            self.base_text = str(self.base_text) + '\n' + str(self.guaranty) + '\n'
        self.base_text = str(self.base_text) + default_text


        tmp_di = self.device_provider
        self.device_provider = False
        #if self.www == True:
        #   BookingProduct.objects.create(product_pka=self,
        #                                  booking_flag=self.booking,
        #                                   sell_flag=self.sell,)
        #self.www = False
        super().save(*args, **kwargs)

        if self.count == 1 or tmp_di:
            BookingProduct.objects.create(product_pka=self,
                                          booking_flag=False,
                                          sell_flag=False,)

        from .views import update_products
        update_products()  # Обновляем товары в боте

    def __str__(self):
        return self.name


class BookingProduct(models.Model):
    product_pka = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    booking_flag = models.BooleanField('Бронь', default=False)
    sell_flag = models.BooleanField('Продажа', default=False)
    phone = models.CharField('Телефон', max_length=13, null=True, blank=True)
    name_user = models.CharField('Имя клиента', max_length=25, null=True, blank=True)


    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронь'


    def save(self, *args, **kwargs):
        Product.objects.filter(id=self.product_pka.id).update(booking=self.booking_flag)
        Product.objects.filter(id=self.product_pka.id).update(sell=self.sell_flag)
        if not self.booking_flag and not self.sell_flag:
            self.phone = ' '
            self.name_user = ' '
        
        super().save(*args, **kwargs)
        from .views import update_products
        update_products()  # Обновляем товары в боте

    def __str__(self):
        return str(self.product_pka)

