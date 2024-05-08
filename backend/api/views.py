from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from api.serializers import ItemsSerializer, BlogSerializer, CategorySerializer
from blog.models import Blog
from category.models import Category
from item.models import Item


class ItemsViewSet(viewsets.ModelViewSet):
    """Вьюсет товаров."""

    queryset = Item.objects.filter(is_published=True).prefetch_related('tags')
    serializer_class = ItemsSerializer
    http_method_names = ['get']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    ordering_fields = ('price', 'discount_price')
    filterset_fields = ('is_discount', 'is_special_offer')
    search_fields = ('^name',)

    def get_queryset(self):
        """Переопределяем получение queryset на случай фильтрации по тегам."""

        queryset = super().get_queryset()
        tags = self.request.query_params.get('tags', False)

        if tags:
            tags_list = tags.split(', ')
            queryset = Item.objects.filter(tags__name__in=tags_list)

        return queryset


class BlogViewSet(viewsets.ModelViewSet):
    """Вьюсет записей в блоге."""

    queryset = Blog.objects.filter(is_published=True).order_by('-id')
    serializer_class = BlogSerializer
    http_method_names = ['get']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^title',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий товаров."""

    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    http_method_names = ['get']


class DiscountViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения распродаж."""

    queryset = Item.objects.filter(
        is_discount=True, discount_price__gt=0, is_published=True
    ).prefetch_related('tags')
    serializer_class = ItemsSerializer
    http_method_names = ['get']


class SpecialOfferViewSet(viewsets.ModelViewSet):
    """Вьюсет специальных предложений."""

    queryset = Item.objects.filter(
        is_special_offer=True, is_published=True
    ).prefetch_related('tags')
    serializer_class = ItemsSerializer
    http_method_names = ['get']
