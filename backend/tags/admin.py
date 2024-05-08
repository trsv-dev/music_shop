from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api.resources import TagsResource
from tags.models import ItemTag, Tags


# @admin.register(ItemTag)
# class TaskTagsAdmin(admin.ModelAdmin):
#     list_display = ('item', 'tag')
#     list_per_page = 25


@admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
class TagsAdmin(ImportExportModelAdmin):
    """Класс администрирования тегов."""

    resource_class = TagsResource
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
