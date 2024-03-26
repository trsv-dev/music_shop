from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from item.models import Item

admin.site.site_header = "Магазин музыкальных инструментов"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать магазин музыкальных инструментов!"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Класс администрирования товаров."""

    list_display = ('id', 'name', 'show_description', 'short_description',
                    'category', 'show_tags', 'show_image', 'is_special_offer',
                    'show_price', 'is_discount', 'show_discount_price',
                    'add_date', 'is_published', 'is_on_main')
    ordering = ('-add_date',)
    search_fields = ('name', 'description')
    list_per_page = 25

    def show_description(self, obj):
        return obj.description if (len(obj.description) <
                                   settings.DESCRIPTION_LENGHT) else (
                obj.description[:settings.DESCRIPTION_LENGHT] + '...')

    show_description.short_description = 'Описание'

    def show_tags(self, obj):
        tag_names = [tag.name for tag in obj.tags.filter(items=obj)]
        return tag_names

    show_tags.short_description = 'Теги'

    def show_price(self, obj):
        return f'{obj.price:,} руб.'

    show_price.short_description = 'Цена без акции'
    show_price.admin_order_field = 'price'

    def show_discount_price(self, obj):
        return f'{obj.discount_price:,} руб.' if obj.discount_price else f'{0} руб.'

    show_discount_price.short_description = 'Цена по акции'
    show_discount_price.admin_order_field = 'discount_price'

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'
