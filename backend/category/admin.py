from django.contrib import admin

from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс администрирования категорий."""

    list_display = ('name', 'slug', 'short_description', 'show_image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'short_description')
    ordering = ('name',)
    list_per_page = 25

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; '
                'object-fit: cover;" />', obj.image.url
            )
        return 'Нет изображения'

    show_image.short_description = 'Изображение'
