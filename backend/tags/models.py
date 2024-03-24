from django.core.validators import RegexValidator
from django.db import models


class Tags(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег'
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

    class Meta:
        verbose_name = 'Создать тег'
        verbose_name_plural = 'Создать теги'

    def __str__(self):
        return self.name


class ItemTag(models.Model):
    """Модель для сопоставления товаров и тегов."""

    item_model_name = 'item.Item'

    item = models.ForeignKey(
        item_model_name,
        on_delete=models.CASCADE,
        related_name='item_tags',
        verbose_name='Товар',
        help_text='Выберите товар'

    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='Выберите тег'
    )

    class Meta:
        verbose_name = 'Присвоить тег'
        verbose_name_plural = 'Присвоить теги'
        constraints = (
            models.UniqueConstraint(
                fields=('item', 'tag'),
                name='unique_item_tag'
            ),
        )

    def __str__(self):
        return f'Товару "{self.item}" присвоен тег "{self.tag}"'
