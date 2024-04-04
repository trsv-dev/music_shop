from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from api.views import (ItemsViewSet, BlogViewSet, CategoryViewSet,
                       DiscountViewSet, SpecialOfferViewSet)
from order.views import CartView, AddToCartView, DeleteCartView, \
    UpdateCartView, CheckoutView


schema_view = get_schema_view(
   openapi.Info(
      title="Music Shop API",
      default_version='v1',
      description="Документация для API музыкального магазина",
      contact=openapi.Contact(email="tarasov.itc@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

router.register('items', ItemsViewSet, basename='items')
router.register('blog', BlogViewSet, basename='blog')
router.register('categories', CategoryViewSet, basename='categories')
router.register('discount', DiscountViewSet, basename='discount')
router.register('special_offer', SpecialOfferViewSet, basename='special_offer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/cart/', CartView.as_view(), name='cart'),
    path('api/v1/add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('api/v1/delete_cart/', DeleteCartView.as_view(), name='delete_cart'),
    path('api/v1/update_cart/', UpdateCartView.as_view(), name='update_cart'),
    path('api/v1/checkout/', CheckoutView.as_view(), name='update_cart'),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += [
        re_path(
            r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'
        ),
        path(
            'swagger/',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
        ),
        path(
            'redoc/',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'
        ),
    ]
