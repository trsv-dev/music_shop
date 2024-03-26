from rest_framework import viewsets

from api.serializers import ItemsSerializer, BlogSerializer, CategorySerializer
from blog.models import Blog
from category.models import Category
from item.models import Item


class ItemsViewSet(viewsets.ModelViewSet):
    """Вьюсет товаров."""

    queryset = Item.objects.filter(is_published=True).prefetch_related('tags')
    serializer_class = ItemsSerializer


class BlogViewSet(viewsets.ModelViewSet):
    """Вьюсет записей в блоге."""

    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий товаров."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DiscountViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения распродаж."""

    queryset = Item.objects.filter(
        is_discount=True, discount_price__gt=0, is_published=True
    ).prefetch_related('tags')
    serializer_class = ItemsSerializer


class SpecialOfferViewSet(viewsets.ModelViewSet):
    """Вьюсет специальных предложений."""

    queryset = Item.objects.filter(
        is_special_offer=True, is_published=True
    ).prefetch_related('tags')
    serializer_class = ItemsSerializer
