from django.db import models


class FAQModel(models.Model):
    name = models.CharField('Имя кнопки', max_length=255)
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Не обязательно',
        upload_to='media_faq',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
    )

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.name
