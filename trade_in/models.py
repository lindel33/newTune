from django.db import models


class TelegramUserModel(models.Model):
    user_id = models.CharField('Id пользователя', max_length=25)
    username = models.CharField('Ник пользователя', max_length=255, null=True)
    first_name = models.CharField('Имя пользователя', max_length=255, null=True)
    date_registered = models.DateField('Дата регистрации', auto_now=True)

    
    def __str__(self):
        return self.username


class UserStepModel(models.Model):
    user = models.ForeignKey(TelegramUserModel,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    steps_ok = models.CharField('Текущий шаг',
                                max_length=2)
    cost = models.IntegerField('Текущая оценка',
                               default=0)
    device = models.CharField('Текущее устройство',
                              max_length=50)


class TradeInDevicesModel(models.Model):
    name = models.CharField('Название кнопки', max_length=20)

    class Meta:
        verbose_name = 'Главные кнопки'
        verbose_name_plural = 'Главные кнопки'

    def __str__(self):
        return self.name


class TradeInSeriesModel(models.Model):
    name = models.CharField('Название серии', max_length=20)
    start_cost = models.IntegerField('Начальная цена', default=0)
    max_step = models.IntegerField('Всего шагов')
    objects = models.Manager()
    
    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def __str__(self):
        return self.name


class VariableFoeStepModel(models.Model):
    name = models.CharField('Название выбора',
                            max_length=50)
    increase = models.IntegerField('Увеличение при выборе на', default=0)
    decrease = models.IntegerField('Уменьшение при выборе на', default=0)
    step = models.ForeignKey('TradeInStepModel',
                             on_delete=models.CASCADE,
                             verbose_name='Номер шага',
                             )

    class Meta:
        verbose_name = 'Выбор'
        verbose_name_plural = 'Выбор'

    def __str__(self):
        return self.name


ch_num = [('1', '1'),
          ('2', '2'),
          ('3', '3'),
          ('4', '4'),
          ('5', '5'),
          ('6', '6'),
          ('7', '7'),
          ('8', '8'),
          ('9', '9'),
          ('10', '10'),
          ]


class TradeInStepModel(models.Model):
    """Шаги для устройств"""
    step = models.CharField('Номер шага',
                            choices=ch_num,
                            max_length=10)
    name = models.CharField('Название шага',
                            max_length=60)
    series = models.ForeignKey(TradeInSeriesModel,
                               on_delete=models.CASCADE,
                               verbose_name='Шаг для')

    class Meta:
        verbose_name = 'Шаги'
        verbose_name_plural = 'Шаги'

    def __str__(self):
        return self.name


