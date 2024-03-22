from django.contrib import admin
from django.utils.html import format_html

from item.models import Item


@admin.register(Item)
class ItemsAdmin(admin.ModelAdmin):
    """Класс администрирования товаров."""

    list_display = ('id', 'name', 'description',
                    'show_image', 'add_date', 'is_published', 'is_on_main')
    ordering = ('-add_date',)
    search_fields = ('name', 'description')
    list_per_page = 25

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'
