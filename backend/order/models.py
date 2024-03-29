import random
import string

from django.db import models

from item.models import Item


class Order(models.Model):
    """Модель заказов."""

    order_number = models.CharField(
        default=0,
        max_length=10,
        editable=False,
        verbose_name='Идентификатор заказа'
    )
    first_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Фамилия',
        help_text='Введите фамилию'
    )
    address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Адрес',
        help_text='Введите ваш адрес в формате "город, улица, дом, корпус, '
                  'квартира"'
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
        verbose_name='email',
        help_text='Введите электронную почту'
    )
    communication_method = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Способ связи',
        help_text='Укажите предпочтительный способ связи (необязательно)'
    )
    items = models.ManyToManyField(
        Item,
        through='OrderItem',
    )
    order_notes = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Примечания к заказу',
        help_text='Напишите ваши дополнительные пожелания (необязательно)'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время добавления'
    )

    @classmethod
    def generate_order_number(cls):
        """Генерируем уникальный номер заказа."""

        alphabet_lowercase = string.ascii_lowercase
        alphabet_uppercase = string.ascii_uppercase
        numbers = '123456789'

        return ''.join(random.sample(
            list(alphabet_lowercase + alphabet_uppercase + numbers), 10))

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ "{str(self.order_number)}"'


class OrderItem(models.Model):
    """Модель для связи товаров и заказа."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        help_text='Выберите заказ'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        help_text='Выберите товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
        help_text='Введите количество'
    )

    class Meta:
        unique_together = ['order', 'item']
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'Товар в заказе'
