from rest_framework import serializers

from blog.models import Blog
from category.models import Category
from item.models import Item


class ItemsSerializer(serializers.ModelSerializer):
    """Сериализатор товаров."""

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'short_description',
                  'category', 'tags', 'image', 'is_special_offer', 'price',
                  'is_discount', 'discount_price', 'add_date', 'is_published',
                  'is_on_main']


class BlogSerializer(serializers.ModelSerializer):
    """Сериализатор для записей в блоге."""

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'text', 'add_date', 'is_published']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий товаров."""

    class Meta:
        model = Category
        fields = ['name', 'slug', 'short_description', 'image']
