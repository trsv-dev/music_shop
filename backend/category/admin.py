from django.contrib import admin
from django.utils.html import format_html

from category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс администрирования категорий."""

    fields = ('name', 'slug', 'short_description', 'image',
              'show_image_preview')
    list_display = ('name', 'slug', 'short_description', 'show_image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'short_description')
    readonly_fields = ('show_image_preview',)
    ordering = ('name',)
    list_per_page = 25

    def show_image(self, obj):
        """Отображение изображения категории."""

        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'

    def show_image_preview(self, obj):
        """Превью изображения категории при редактировании."""

        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 250px; max-height: 250px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image_preview.short_description = 'Превью'
