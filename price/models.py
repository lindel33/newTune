from pprint import pprint

from django.db import models


class Global(models.Model):
    """
    Страны, цвета
    """
    country = models.TextField('Флаг страны', null=False, blank=False)
    color = models.TextField('Цвет', null=False, blank=False)

    class Meta:
        verbose_name = 'Глобальные установки'
        verbose_name_plural = 'Глобальные установки'

    def __str__(self):
        return 'Цвета/Страны'


class Iphone(models.Model):
    memory = models.TextField('Память', help_text='16, 16гб, 16gb, 16гб...')
    series_prefix = models.TextField('Модели с префиксом', help_text='11 pro, 11 pro max...')
    series_not_prefix = models.TextField('Модели без префикса и букв', help_text='6, 7, 8, 11, 12, 13')
    extra_iphone = models.TextField('Extra модели', help_text='se, sr, x, xs')
    full_name = models.TextField('Полное название', help_text='iphone 8, iphone x, iphone 11')

    class Meta:
        verbose_name = 'iPhone'
        verbose_name_plural = 'iPhone'

    def __str__(self):
        return 'iPhone'


class Markup(models.Model):
    name_models = models.CharField('Устройство', max_length=10)
    markup = models.SmallIntegerField('Процент наценки')
    flag = models.BooleanField('Счет в процентах?', default=False)
    markup_int = models.SmallIntegerField('Наценка в рублях', null=True)

    class Meta:
        verbose_name = 'Наценка'
        verbose_name_plural = 'Наценки'

    def __str__(self):
        return str(self.name_models)


class Ipad(models.Model):
    memory = models.TextField('Память', help_text='16,16гб,16 gb,16 гб...')
    series = models.TextField('Модели с префиксом', help_text='iPad pro,iPad mini...')
    names = models.TextField('WiFi', help_text='Wi-Fi + Cellular...')
    numbers = models.TextField('Полное название', help_text='iPad 12.iPad 9,iPad 11')

    class Meta:
        verbose_name = 'iPad'
        verbose_name_plural = 'iPad'

    def __str__(self):
        return 'iPad'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


class MacBook(models.Model):
    memory = models.TextField('Память', help_text='16gb,16гб,16 gb,16 гб...')
    series = models.TextField('Модели с префиксом', help_text='MacBook Pro,MacBook Air...')
    names = models.TextField('WiFi', help_text='M1')
    extra = models.TextField('Полное название', help_text='MacBook 11, MacBook Pro 12')

    class Meta:
        verbose_name = 'MacBook'
        verbose_name_plural = 'MacBook'

    def __str__(self):
        return 'MacBook'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


class Watch(models.Model):
    size = models.TextField('Размер', help_text='44mm, 45mm')
    size_exists = models.TextField('Размер без mm', help_text='44,45')
    series = models.TextField('Серии', help_text='5,6,7...')
    series_full_names = models.TextField('Серии', help_text='Series 3, Series 4')
    extra = models.TextField('Extra имена', help_text='SE...')

    class Meta:
        verbose_name = 'Watch'
        verbose_name_plural = 'Watch'

    def __str__(self):
        return 'Watch'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


class MacBook1(models.Model):
    memory = models.TextField('Память', help_text='16, 16гб, 16gb, 16гб...')
    series = models.TextField('Модели с префиксом', help_text='MacBook Pro,MacBook Air...')
    names = models.TextField('Extra', help_text='M1')
    extra = models.TextField('Полное название', help_text='MacBook 11, MacBook Pro 12')

    class Meta:
        verbose_name = 'MacBook'
        verbose_name_plural = 'MacBook'

    def __str__(self):
        return 'MacBook'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


class SpecialCharacter(models.Model):
    provider_variant = models.CharField('Вариант поставщика', max_length=30)
    new_variant = models.CharField('Вариант на сайте', max_length=30)

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return 'Вариация'
