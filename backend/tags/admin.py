from django.contrib import admin

from tags.models import ItemTag, Tags


# @admin.register(ItemTag)
# class TaskTagsAdmin(admin.ModelAdmin):
#     list_display = ('item', 'tag')
#     list_per_page = 25


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """Класс администрирования тегов."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
