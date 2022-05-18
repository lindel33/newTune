from django.db import models

class Trade(models.Model):
    name_button = models.CharField(verbose_name='Кнопка в боте',
                                   max_length=50)
    image_1 = models.ImageField('Картинка 1',
                                upload_to='trade',
                                null=False,
                                )
    image_2 = models.ImageField('Картинка 2',
                                upload_to='trade',
                                null=False,
                                )
    text = models.TextField('Текст')
    
    class Meta:
        verbose_name = 'Обменка'
        verbose_name_plural = 'Обменки'
        
    def __str__(self):
        return self.name_button
