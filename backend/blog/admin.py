from django.conf import settings
from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Класс администрирования записей в блоге."""

    list_display = ('title', 'slug', 'show_text', 'add_date', 'is_published')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-add_date',)
    list_per_page = 25

    def show_text(self, obj):
        return obj.text if (len(obj.text) <
                            settings.BLOG_TEXT_LENGHT) else (
                obj.text[:settings.BLOG_TEXT_LENGHT] + '...')

    show_text.short_description = 'Текст записи'
