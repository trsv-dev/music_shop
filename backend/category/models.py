from django.core.validators import RegexValidator
from django.db import models


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='В слаге содержится недопустимый символ'
            ),
        ),
        verbose_name='Слаг'
    )
    short_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Краткое описание категории',
        help_text='Введите краткое описание категории'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/categories/',
        verbose_name='Изображение категории',
        help_text='Загрузите изображение категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
