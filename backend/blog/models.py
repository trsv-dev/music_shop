from django.core.validators import RegexValidator
from django.db import models


class Blog(models.Model):
    """Модель блога."""

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Заголовок',
        help_text='Введите заголовок записи в блоге'
    )
    slug = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='В слаге содержится недопустимый символ'
            ),
        ),
        verbose_name='Слаг'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст записи',
        help_text='Введите текст записи в блоге'
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время добавления'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано?',
        help_text='Отметить запись как опубликованную?',
        choices=(
            (True, 'Да'),
            (False, 'Нет')
        )
    )

    class Meta:
        verbose_name = 'Запись в блогe'
        verbose_name_plural = 'Записи в блоге'

    def __str__(self):
        return self.title
