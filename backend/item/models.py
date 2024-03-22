from django.db import models


class Item(models.Model):
    """Модель товаров."""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Название',
        help_text='Введите название товара'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание товара'
    )
    image = models.ImageField(
        default=None,
        null=True,
        blank=True,
        upload_to='images/items/',
        verbose_name='Изображение',
        help_text='Загрузите изображение'
    )
    add_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата и время добавления'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано?',
        help_text='Отметить товар как опубликованный?',
        choices=(
            (True, 'Да'),
            (False, 'Нет')
        )
    )
    is_on_main = models.BooleanField(
        default=False,
        verbose_name='На главной странице?',
        help_text='Разместить на главной странице?',
        choices=(
            (True, 'Да'),
            (False, 'Нет')
        )
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-add_date',)

    def __str__(self):
        return f'Добавлен товар "{self.name}"'
