from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from order.models import Order, OrderItem


class ItemsInLine(admin.TabularInline):
    """Класс для отображения товаров в заказе внутри 'OrderAdmin'."""

    model = OrderItem
    extra = 0
    ordering = ('id',)
    readonly_fields = ('show_image_preview', 'price_per_item',
                       'price_for_all_items',)

    def __init__(self, model, admin_site):
        """
        Конструктор класса. Используем для добавления атрибута 'self.request'.
        """

        self.request = None
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        """
        Переопределяем метод для добавления в атрибут
        класса 'self.request' админского 'request'.
        """

        self.request = request
        return super().get_queryset(request)

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

    def show_image_preview(self, obj):
        """Показать превью изображения товара в заказе."""

        # Получаем 'request' администратора благодаря переопределенному
        # 'get_queryset'.
        request = self.request
        show_preview = request.session.get('show_preview', False)
        if show_preview:
            image = obj.item.image
            if image:
                return format_html(
                    '<img src="{}" '
                    'style="max-width: 180px; max-height: 180px; '
                    'object-fit: cover;" />', image.url
                )
        return 'Превью отключены'
    show_image_preview.short_description = 'Превью'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс администрирования заказов."""

    list_display = ('id', 'order_number', 'status', 'first_name', 'last_name',
                    'total_price', 'email',
                    'show_items_quantity_in_cart',
                    'show_items_total_quantity',
                    'show_order_notes', 'show_admin_notes', 'created_date')
    ordering = ('-created_date',)
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('first_name', 'order_number', 'last_name', 'address',
                     'email', 'communication_method')
    inlines = (
        ItemsInLine,
    )
    list_per_page = 25
    # "Уменьшаем" размер текстовых полей.
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3})},
    }

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

    def response_change(self, request, obj):
        """
        Переопределяем порядок действий при редактировании заказа, а
        конкретнее - при нажатии на кнопку "Вкл./выкл. превью" включается или
        отключается отображение изображений в заказе.
        Заказ остается на странице редактирования.
        """
        if '_show_preview' in request.POST:
            show_preview = request.session.get('show_preview', False)
            request.session['show_preview'] = not show_preview
            if show_preview:
                self.message_user(request, 'Отображение изображений '
                                           'товара в заказе выключено')
            else:
                self.message_user(request, 'Отображение изображений '
                                           'товара в заказе включено')

            # Остаемся на текущей странице если редактируем.
            # Если сохраняем, то поведение без изменений.
            if '_save' in request.POST:
                pass

            return HttpResponseRedirect(request.path_info)
        return super().response_change(request, obj)
