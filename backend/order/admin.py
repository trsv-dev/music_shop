from django.conf import settings
from django.contrib import admin

from order.models import Order


class ItemsInLine(admin.TabularInline):
    model = Order.items.through
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс администрирования заказов."""

    list_display = ('id', 'order_number', 'first_name', 'last_name', 'address',
                    'email', 'get_order_items', 'communication_method',
                    'show_order_notes', 'created_date')
    ordering = ('-created_date',)
    search_fields = ('first_name', 'last_name', 'address',
                     'email', 'communication_method')
    inlines = (
        ItemsInLine,
    )
    list_per_page = 25

    def show_order_notes(self, obj):
        """Отображение укороченных примечаний к заказу."""

        if obj.order_notes:
            return obj.order_notes if (len(obj.order_notes) <
                                       settings.ORDER_NOTES_LENGHT) else (
                    obj.order_notes[:settings.ORDER_NOTES_LENGHT] + '...')

    show_order_notes.short_description = 'Примечания к заказу'

    def get_order_items(self, obj):
        """Отображение товаров в заказе"""

        # return '\n'.join(item.name for item in obj.items.all())
        return len(obj.items.all())

    get_order_items.short_description = 'Товаров в заказе'

