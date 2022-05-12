from django.db import models
from trade_in.models import TelegramUserModel


class ButtonModel(models.Model):
    """Таблица устройств серии"""
    name_button = models.CharField('Имена кнопок',
                                   max_length=255)

    class Meta:
        verbose_name = 'Имена кнопок'
        verbose_name_plural = 'Имена кнопок'

    def __str__(self):
        return self.name_button


class ServiceModels(models.Model):
    """Таблица услуг по ремонту"""
    series = models.ForeignKey(ButtonModel,
                               on_delete=models.CASCADE,
                               verbose_name='Услуга для')
    name = models.CharField('Название услуги',
                            max_length=255)
    time_process = models.SmallIntegerField('Время исполнения')
    cost = models.IntegerField('Цена за услугу')

    class Meta:
        verbose_name = 'Услуга по ремонту'
        verbose_name_plural = 'Услуги по ремонту'

    def __str__(self):
        return self.name


class UserChoiceModel(models.Model):
    user_id = models.ForeignKey(TelegramUserModel,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    device = models.CharField('Устройство для ремонта',
                              max_length=100)
    cost = models.SmallIntegerField('Общаяя цена',)

    class Meta:
        verbose_name = 'Пользовательские выборы'


class UseService(models.Model):
    user = models.ForeignKey(UserChoiceModel,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    name_service = models.CharField('Название услуги',
                                    max_length=100)
