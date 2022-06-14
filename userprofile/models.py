from django.db import models
from django.contrib.auth.models import User

from tune_admin.models import RegionUserModel


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    region = models.ForeignKey(RegionUserModel,
                               on_delete=models.CASCADE,
                               verbose_name='Регион',
                               default=1,
                               null=False,
                               blank=False)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'
