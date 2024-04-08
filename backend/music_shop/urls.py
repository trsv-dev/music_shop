from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework import routers, permissions

from api.views import (ItemsViewSet, BlogViewSet, CategoryViewSet,
                       DiscountViewSet, SpecialOfferViewSet)
from order.views import CartView, AddToCartView, DeleteCartView, \
    UpdateCartView, CheckoutView

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
