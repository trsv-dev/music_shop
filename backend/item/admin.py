from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from django.apps import apps

from item.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Класс администрирования товаров."""

    list_display = ('id', 'name', 'show_description', 'short_description',
                    'category', 'show_tags', 'show_image', 'show_price',
                    'show_promo_price', 'add_date', 'is_published',
                    'is_on_main')
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

    def show_promo_price(self, obj):
        return f'{obj.promo_price:,} руб.'

    show_promo_price.short_description = 'Цена по акции'

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'
