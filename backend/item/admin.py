from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from api.resources import ItemResource
from item.models import Item

admin.site.site_header = "Магазин музыкальных инструментов"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать магазин музыкальных инструментов!"


@admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
class ItemAdmin(ImportExportModelAdmin, ExportActionMixin):
    """Класс администрирования товаров."""

    resource_class = ItemResource
    fields = ('name', 'short_description', 'description', 'category', 'tags',
              'image', 'show_image_preview', 'is_special_offer', 'price',
              'is_discount', 'discount_price', 'is_published', 'is_on_main')
    list_display = ('id', 'show_name', 'show_description',
                    'show_short_description', 'category', 'show_tags',
                    'show_image', 'is_special_offer', 'show_price',
                    'is_discount', 'show_discount_price', 'add_date',
                    'is_published', 'is_on_main')
    readonly_fields = ('show_image_preview',)
    list_filter = ('is_published', 'is_discount', 'is_special_offer')
    ordering = ('-add_date',)
    search_fields = ('name', 'description')
    list_per_page = 25

    def show_name(self, obj):
        """Отображение 'укороченного' описания товара."""

        return obj.name if (len(obj.name) <
                                   settings.NAME_LENGHT) else (
                obj.name[:settings.NAME_LENGHT] + '...')

    show_name.short_description = 'Описание'

    def show_description(self, obj):
        """Отображение 'укороченного' описания товара."""

        return obj.description if (len(obj.description) <
                                   settings.DESCRIPTION_LENGHT) else (
                obj.description[:settings.DESCRIPTION_LENGHT] + '...')

    show_description.short_description = 'Описание'

    def show_short_description(self, obj):
        """Отображение 'укороченного' короткого описания товара."""

        return obj.short_description if (len(obj.short_description) <
                                   settings.SHORT_DESCRIPTION_LENGHT) else (
                obj.short_description[:settings.SHORT_DESCRIPTION_LENGHT] + '...')

    show_short_description.short_description = 'Краткое описание'

    def show_tags(self, obj):
        """Отображение тегов товара."""

        tag_names = [tag.name for tag in obj.tags.filter(items=obj)]
        return tag_names

    show_tags.short_description = 'Теги'

    def show_price(self, obj):
        """Отображение цены с разделителями."""

        return f'{obj.price:,} руб.'

    show_price.short_description = 'Цена без акции'
    show_price.admin_order_field = 'price'

    def show_discount_price(self, obj):
        """Отображение акционной цены с разделителями."""

        return f'{obj.discount_price:,} руб.' if obj.discount_price else f'{0} руб.'

    show_discount_price.short_description = 'Цена по акции'
    show_discount_price.admin_order_field = 'discount_price'

    def show_image(self, obj):
        """Отображение изображения товара."""

        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'

    def show_image_preview(self, obj):
        """Превью изображения товара при редактировании."""

        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 250px; max-height: 250px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image_preview.short_description = 'Превью'
