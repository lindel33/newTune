import datetime
from django.db import models

from tune_admin.models import Category, SeriesCategory, get_deadline, \
        Product, states, choices_kit, choices_guaranty, \
        choices_smile, GuarantyModel, KitModel, StateModel, \
        RegionUserModel
from tune_admin.text_default import text_default

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=4)

default_guaranty = 'Гарантия от магазина на проверку 3 месяца !✅'
default_text = text_default


valid_name_text = """
                      Допустимые форматы:\n<br><br>
                      -- iPhone 13 Pro 128 Silver\n<br>
                      -- iPad mini 6 WiFi Silver\n<br>
                      -- Watch 7 45 Silver\n<br>
                      -- AirPods 3\n<br>
                      -- MacBook Pro 13\n<br>
                      -- MacBook / iMac 2021 24' 8/256<br><br>
                      Для категории 'устройства' формат свободный"""


class ProviderProduct(models.Model):
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
    moderation = models.BooleanField('Допущен к публикации?', default=False)
    price = models.PositiveIntegerField('Цена')

    smile = models.CharField('Эмодзи к цене', max_length=5, choices=choices_smile, null=True, blank=True,
                             help_text='Оставить пустым, если не нужен', default='₽')
    name = models.CharField('Название', max_length=150, null=False,
                            help_text=valid_name_text)
    name_tmp = models.CharField('Фоновое имя', max_length=100, null=False)
    tests = models.BooleanField('Ростест?', default=False)
    article = models.CharField('Код товара', max_length=15, null=False,
                               help_text='Пример: 20X100ZT')
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, verbose_name='Состояние')
    state_akb = models.SmallIntegerField('Состояние АКБ', default=0,
                                         help_text='Оставить в поле 0, если по АКБ нет информации')
    works = models.TextField('Произведенные работы', null=True, blank=True,
                             help_text='Оставить поле пустым, если не нужно')
    kit = models.ForeignKey(KitModel, on_delete=models.CASCADE, verbose_name='Комплект', null=True, blank=True)
    guaranty = models.ForeignKey(GuarantyModel, on_delete=models.CASCADE, verbose_name='Гарантия',blank=True, null=True, default=None)
    custom_guaranty = models.DateField('Своя гарантия', null=True, blank=True)

    base_text = models.TextField('Нижняя подпись к посту', null=False, default=default_text)
    day_created = models.DateTimeField('Дата создания', auto_now_add=True)
    day_next_publish = models.DateTimeField('Дата следующего поста', default=get_deadline)
    regin = models.ForeignKey(RegionUserModel, on_delete=models.CASCADE, null=True, verbose_name='Регион',default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Модель', null=True, blank=True)
    series = models.ForeignKey(SeriesCategory, on_delete=models.CASCADE,
                               verbose_name='Серия', null=True, blank=True)

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, verbose_name='Автор', )
    count = models.SmallIntegerField('Счетчик сохранений', default=0)
    up_price = models.BooleanField('Цена поднята?', default=False)

    provider_device = models.CharField('Поставщик', max_length=50, default='Устройсво клиента', choices=[
        ('Устройсво клиента', 'Устройсво клиента'),
        ('Илья Савичев', 'Илья Савичев'),
        ('Эмиль', 'Эмиль'),
    ],
                                       )
    device_provider = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def clean(self):
        filter_names = ['Watch', 'iPhone', 'AirPods', 'iPad', 'MacBook', r'MacBook / iMac']
        name_ = str(self.name).split()[0]
        if str(self.category) != '⌨ Устройства':
            if name_ not in filter_names:
                if 'imac' == name_.lower():
                    self.name = r'MacBook / ' + str(self.name)
                else:
                    from django.core.exceptions import ValidationError
                    raise ValidationError({'name': 'Не соответствует шаблону'})
    def save(self, extra=None, *args, **kwargs):
        if self.sell:
            Product.objects.filter(article=self.article).update(sell=True)
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
            self.name = str(self.name_tmp) + ' ' + 'Ростест🇷🇺'
        else:
            self.name = str(self.name_tmp)

        self.name = str(self.name) + ' - ' + str(result_price)

        if self.smile:
            self.name = str(self.name) + str(self.smile)

        self.base_text = str(self.name) + '\n\n' + 'Код товара: ' + str(self.article) + '\n\n' \
                         + str(self.state) + '\n'

        self.base_text = str(self.base_text) + '\nКомплект: ' + str(self.kit) + '\n'

        if self.state_akb != 0:
            self.base_text = str(self.base_text) + '\nРодной аккумулятор: ' + str(self.state_akb) + '%\n'

        if self.works:
            self.base_text = str(self.base_text) + '\n' + str(self.works) + '\n'

        if not self.guaranty:
            castom_guarnt = datetime.datetime.strptime(str(self.custom_guaranty), '%Y-%m-%d').strftime('%d-%m-%Y')
            self.base_text = str(self.base_text) + '\nОфициальная гарантия Apple до ' \
                             + str(castom_guarnt) + '\n'
        else:
            self.base_text = str(self.base_text) + '\n' + str(self.guaranty) + '\n'
        self.base_text = str(self.base_text) + default_text
        if self.device_provider:
            res = Product.objects.create(
                image_1=self.image_1,
                image_2=self.image_2,
                image_3=self.image_3,
                sell=False,
                booking=False,
                moderation=False,
                price=self.price,
                smile=self.smile,
                name=self.name,
                name_tmp=self.name_tmp,
                tests=self.tests,
                article=self.article,
                state=self.state,
                state_akb=self.state_akb,
                works=self.works,
                kit=self.kit,
                guaranty=self.guaranty,
                custom_guaranty=self.custom_guaranty,

                base_text=self.base_text,
                day_created=self.day_created,
                day_next_publish=self.day_next_publish,

                category=self.category,
                series=self.series,

                author=self.author,
                count=1,
                up_price=self.up_price,
                regin=self.regin,
                provider_device=self.provider_device,
                device_provider=self.device_provider,

            )
            self.device_provider = False
        super().save(*args, **kwargs)
        import telebot
        from tune_admin.models import UserModel
        admins = UserModel.objects.filter(super_user=True, provider_notifications=True).values_list('user_id')
        admins = [i[0] for i in admins]
        token = '5239855839:AAFeQBXF4EmVJK7DDy6RN9rPeIIgskPWLig'
        path_to_media = '/home/apple/code/project1/tune/media/'
        client = telebot.TeleBot(token=token)
        for chat_id in admins:
                if self.image_3:
                    f1, f2, f3 = open(path_to_media + str(self.image_1), 'rb'), \
                                 open(path_to_media + str(self.image_2), 'rb'), \
                                 open(path_to_media + str(self.image_3), 'rb')
                    f1, f2, f3 = f1.read(), f2.read(), f3.read()
                    client.send_media_group(chat_id=chat_id, media=[
                        telebot.types.InputMediaPhoto(f1, caption=self.base_text, parse_mode='HTML'),
                        telebot.types.InputMediaPhoto(f2),
                        telebot.types.InputMediaPhoto(f3), ])
                else:
                    f1, f2 = open(path_to_media + str(self.image_1), 'rb'), \
                                 open(path_to_media + str(self.image_2), 'rb')
                    f1, f2 = f1.read(), f2.read()
                    client.send_media_group(chat_id=chat_id, media=[
                        telebot.types.InputMediaPhoto(f1, caption=self.base_text, parse_mode='HTML'),
                        telebot.types.InputMediaPhoto(f2),])
                info = f'Категория: {self.category}' \
                       f'\nСерия: {self.series}'
                client.send_message(chat_id=chat_id,
                                    text=f'Товар создал: {self.author}' + '\n\n' + info)
                out = [
                    [f'🔑✅ Допустить пост к публикации id={res.id}'],
                    [f'🔑↪️ Отложить рассмотрение id={res.id}'],
                    [f'🔑❌ УДАЛИТЬ ПОСТ (БЕЗВОЗРАТНО) id={res.id}'],
                    ['⬅️Главное меню']
                ]
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.keyboard = out
                client.send_message(chat_id=chat_id,
                                    text='Что сделать с постом?',
                                    reply_markup=keyboard)

    def __str__(self):
        return self.name

