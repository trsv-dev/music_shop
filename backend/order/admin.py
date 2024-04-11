from django.conf import settings
from django.contrib import admin

from order.models import Order, OrderItem


class ItemsInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    ordering = ('id',)
    readonly_fields = ('price_per_item', 'price_for_all_items',)

    def price_for_all_items(self, obj):
        """
        Отображает общую стоимость товара в зависимости
        от его количества в заказе.
        """

        return f'{(obj.item.discount_price if obj.item.is_discount else obj.item.price) * obj.quantity:,} руб.'

    price_for_all_items.short_description = 'Общая стоимость'

    def price_per_item(self, obj):
        """Отображение стоимости одной единицы товара."""

        return f'{obj.item.discount_price if obj.item.is_discount else obj.item.price:,} руб.'

    price_per_item.short_description = 'Стоимость за единицу'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс администрирования заказов."""

    list_display = ('id', 'order_number', 'status', 'first_name', 'last_name',
                    'total_price', 'address', 'email',
                    'show_items_quantity_in_cart',
                    'show_items_total_quantity', 'communication_method',
                    'show_order_notes', 'show_admin_notes', 'created_date')
    ordering = ('-created_date',)
    list_filter = ('status',)
    search_fields = ('first_name', 'order_number', 'last_name', 'address',
                     'email', 'communication_method')
    inlines = (
        ItemsInLine,
    )
    list_per_page = 25

    def total_price(self, obj):
        """Отображение полной стоимости заказа."""

        return f'{sum((item.item.discount_price if item.item.is_discount else item.item.price) * item.quantity for item in obj.orderitem_set.all()):,} руб.'

    total_price.short_description = 'Полная стоимость'

    def show_order_notes(self, obj):
        """Отображение укороченных примечаний к заказу."""

        if obj.order_notes:
            return obj.order_notes if (len(obj.order_notes) <
                                       settings.ORDER_NOTES_LENGHT) else (
                    obj.order_notes[:settings.ORDER_NOTES_LENGHT] + '...')

    show_order_notes.short_description = 'Примечания к заказу'

    def show_admin_notes(self, obj):
        """Отображение укороченных примечаний для администратора."""

        if obj.admin_notes:
            return obj.admin_notes if (len(obj.admin_notes) <
                                       settings.ADMIN_NOTES_LENGHT) else (
                    obj.admin_notes[:settings.ADMIN_NOTES_LENGHT] + '...')

    show_admin_notes.short_description = 'Примечания админа'

    def show_items_quantity_in_cart(self, obj):
        """Отображение количества наименований в заказе"""

        # return '\n'.join(item.name for item in obj.items.all())
        return len(obj.items.all())

    show_items_quantity_in_cart.short_description = 'Наименований'

    def show_items_total_quantity(self, obj):
        """Отображение общего количества товаров в заказе."""

        return sum(item.quantity for item in obj.orderitem_set.all())

    show_items_total_quantity.short_description = 'Общее количество'
