from import_export import resources
from import_export.fields import Field

from category.models import Category
from item.models import Item
from order.models import Order
from tags.models import Tags


class TagsResource(resources.ModelResource):
    """Класс импорта / экспорта тегов."""

    class Meta:
        model = Tags


class ItemResource(resources.ModelResource):
    """Класс импорта / экспорта товаров."""

    class Meta:
        model = Item


class CategoryResource(resources.ModelResource):
    """Класс импорта / экспорта категорий."""

    class Meta:
        model = Category


class OrderResource(resources.ModelResource):
    """Класс экспорта заказов."""

    items_names = Field(
        column_name='items_names',
        dehydrate_method='get_items_names',
    )

    def get_items_names(self, instance):
        """
        Получение списка названий товаров
        (возможно благодаря добавлению 'item' к начальному queryset в
        'get_queryset' в admin.py)
        """

        return ', '.join(item.name for item in instance.items.all())

    class Meta:
        model = Order
        export_order = ('id', 'order_number', 'status', 'first_name',
                        'last_name', 'address', 'email',
                        'communication_method', 'items', 'items_names',
                        'order_notes', 'admin_notes', 'created_date')
