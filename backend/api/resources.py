from import_export import resources, widgets
from import_export.fields import Field
from rest_framework.generics import get_object_or_404
from django.utils import timezone

from category.models import Category
from item.models import Item
from order.models import Order
from tags.models import Tags


class TagsResource(resources.ModelResource):
    """Класс импорта / экспорта тегов."""

    id = Field(attribute='id', column_name='ID')
    name = Field(attribute='name', column_name='Название тега')
    slug = Field(attribute='slug', column_name='Слаг')

    class Meta:
        model = Tags


class ItemResource(resources.ModelResource):
    """Класс импорта / экспорта товаров."""

    id = Field(attribute='id', column_name='ID')
    name = Field(attribute='name', column_name='Название')
    short_description = Field(
        attribute='short_description', column_name='Короткое описание'
    )
    description = Field(attribute='description', column_name='Описание')
    category = Field(
        attribute='category',
        column_name='Категория',
        widget=widgets.ForeignKeyWidget(Category, field='name'))
    tags = Field(
        attribute='tags',
        column_name='Теги',
        widget=widgets.ManyToManyWidget(Tags, field='name', separator=', ')
    )
    image = Field(attribute='image', column_name='Изображение')
    is_special_offer = Field(
        dehydrate_method='get_is_special_offer',
        column_name='Уникальное предложение?'
    )
    price = Field(attribute='price', column_name='Цена без распродажи')
    is_discount = Field(dehydrate_method='get_is_discount',
                        column_name='Распродажа?')
    discount_price = Field(
        attribute='discount_price', column_name='Цена при распродаже'
    )
    add_date = Field(
        dehydrate_method='get_add_date', column_name='Дата добавления'
    )
    is_published = Field(dehydrate_method='get_is_published', column_name='Опубликовано?')
    is_on_main = Field(dehydrate_method='get_is_on_main', column_name='На главной?')

    def before_import_row(self, row, **kwargs):
        """Преобразования перед импортом."""

        # Заменяем 'Да' и 'Нет' на 'True' и 'False'.
        row['Уникальное предложение?'] = True if (
                row['Уникальное предложение?'] == 'Да') else False
        row['Распродажа?'] = True if row['Распродажа?'] == 'Да' else False
        row['Опубликовано?'] = True if row['Опубликовано?'] == 'Да' else False
        row['На главной?'] = True if row['На главной?'] == 'Да' else False

    def get_is_special_offer(self, instance):

        return 'Да' if instance.is_special_offer else 'Нет'

    def get_is_discount(self, instance):

        return 'Да' if instance.is_discount else 'Нет'

    def get_is_published(self, instance):

        return 'Да' if instance.is_published else 'Нет'

    def get_is_on_main(self, instance):

        return 'Да' if instance.is_on_main else 'Нет'

    def get_add_date(self, instance):
        """Получение форматированного времени создания заказа."""

        return timezone.localtime(
            instance.add_date).strftime("%d %B %Y г. %H:%M")

    class Meta:
        model = Item
        exclude = ('id',)


class CategoryResource(resources.ModelResource):
    """Класс импорта / экспорта категорий."""

    id = Field(attribute='id', column_name='ID')
    name = Field(attribute='name', column_name='Название категории')
    slug = Field(attribute='slug', column_name='Слаг')
    short_description = Field(
        attribute='short_description',
        column_name='Короткое описание'
    )
    image = Field(attribute='image', column_name='Изображение')

    class Meta:
        model = Category


class OrderResource(resources.ModelResource):
    """Класс экспорта заказов."""

    # Определяем для полей, которые не были переопределены русские названия.
    items = Field(column_name='ID товара', dehydrate_method='get_item_ids')
    id = Field(attribute='id', column_name='ID')
    order_number = Field(attribute='order_number', column_name='ID заказа')
    status = Field(attribute='status', column_name='Статус заказа')
    first_name = Field(attribute='first_name', column_name='Имя')
    last_name = Field(attribute='last_name', column_name='Фамилия')
    address = Field(attribute='address', column_name='Адрес')
    communication_method = Field(attribute='communication_method',
                                 column_name='Способ связи')
    order_notes = Field(attribute='order_notes', column_name='Пожелания')
    admin_notes = Field(attribute='admin_notes', column_name='Заметки админа')
    created_date = Field(
        column_name='Дата создания', dehydrate_method='get_created_date'
    )
    items_names_and_quantities = Field(
        column_name='Название и количество',
        dehydrate_method='get_items_names_and_quantities',
    )
    items_quantity_in_cart = Field(
        column_name='Наименований в корзине',
        dehydrate_method='get_items_quantity_in_cart'
    )
    items_total_quantity = Field(
        column_name='Общее количество товаров',
        dehydrate_method='get_items_total_quantity'
    )
    total_price = Field(
        column_name='Общая стоимость',
        dehydrate_method='get_total_price'
    )

    def get_total_price(self, instance):
        """Отображение полной стоимости заказа."""

        return f'{sum((orderitem.item.discount_price if orderitem.item.is_discount else orderitem.item.price) * orderitem.quantity for orderitem in instance.orderitem_set.all()):,} руб.'

    def get_item_ids(self, instance):
        """Получение ID товаров в корзине."""

        return ', '.join(f'{orderitem.item.pk}' for
                         orderitem in instance.orderitem_set.all())

    def get_created_date(self, instance):
        """Получение форматированного времени создания заказа."""

        return instance.created_date.strftime('%d %B %Y г. %H:%M')

    def get_items_names_and_quantities(self, instance):
        """
        Получение списка названий товаров
        (благодаря добавлению 'item' к начальному queryset в
        'get_queryset' в admin.py)
        """

        name_quantity = [
            (f'{orderitem.item.name} - {orderitem.quantity} шт. '
             f'({orderitem.item.discount_price if orderitem.item.is_discount else orderitem.item.price:,} руб./шт.)') for
            orderitem in instance.orderitem_set.all()]

        return ', '.join(name_quantity)

    def get_items_quantity_in_cart(self, instance):
        """Получение количества наименований товаров в корзине."""

        return len(instance.items.all())

    def get_items_total_quantity(self, instance):
        """Получение общего количества товаров в корзине."""

        return sum(
            orderitem.quantity for orderitem in instance.orderitem_set.all()
        )

    class Meta:
        model = Order
        export_order = ('id', 'order_number', 'status', 'first_name',
                        'last_name', 'address', 'email',
                        'communication_method', 'items',
                        'items_names_and_quantities',
                        'items_quantity_in_cart', 'items_total_quantity',
                        'order_notes', 'admin_notes', 'total_price',
                        'created_date')
