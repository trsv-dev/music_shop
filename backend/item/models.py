from django.db import models

from category.models import Category


class Item(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Название',
        help_text='Введите название товара'
    )
    short_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Краткое описание',
        help_text='Введите краткое описание товара'
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание',
        help_text='Введите описание товара'
    )
    category = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    tags = models.ManyToManyField(
        'tags.Tags',
        related_name='items',
        verbose_name='Теги'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/items/',
        verbose_name='Изображение',
        help_text='Загрузите изображение'
    )
    is_special_offer = models.BooleanField(
        default=False,
        verbose_name='Уникальное предложение?',
        help_text='Лимитированная серия? / уникальное предложение?',
        choices=(
            (True, 'Да'),
            (False, 'Нет')
        )
    )
    price = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Цена без распродажи',
        help_text='Введите цену без распродажи'
    )
    is_discount = models.BooleanField(
        default=False,
        verbose_name='Распродажа?',
        help_text='Участвует в распродаже?',
        choices=(
            (True, 'Да'),
            (False, 'Нет')
        )
    )
    discount_price = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='Цена при распродаже',
        help_text='Введите цену при распродаже'
    )
    add_date = models.DateTimeField(
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
        return f'{self.category} 🡢 {self.name}'
