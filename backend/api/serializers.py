from rest_framework import serializers

from blog.models import Blog
from category.models import Category
from item.models import Item
from order.models import Order


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


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказов."""

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'email',
                  'communication_method', 'order_notes', ]


class AddToCartSerializer(serializers.Serializer):
    """
    Сериализатор добавления товаров в корзину:
    id товара и quantity (количества товара).
    """

    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_item_id(self, item_id):
        """
        Проверка, что item_id - неотрицательное число.
        Проверка, что item_id существует в БД.
        """

        if item_id <= 0:
            raise serializers.ValidationError('Идентификатор товара не может '
                                              'быть равен нулю или быть '
                                              'отрицательным числом')

        if not Item.objects.filter(id=item_id).exists():
            raise serializers.ValidationError('Товар с таким идентификатором '
                                              'не найден')

        return item_id

    def validate_quantity(self, quantity):
        """Проверка, что quantity - неотрицательное число (int)."""

        if quantity <= 0:
            raise serializers.ValidationError('Количество добавляемых товаров '
                                              'не может быть равно нулю или '
                                              'быть отрицательным числом')

        if not isinstance(quantity, int):
            raise serializers.ValidationError('Количество товара должно быть '
                                              'целым числом')

        return quantity


class UpdateCartSerializer(AddToCartSerializer):
    """
    Сериализатор изменения количества товаров в корзине:
    id товара.
    """

    def validate_quantity(self, quantity):

        if not isinstance(quantity, int):
            raise serializers.ValidationError('Количество товара должно быть '
                                              'целым числом')

        return quantity
