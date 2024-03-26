from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import (ItemsViewSet, BlogViewSet, CategoryViewSet,
                       DiscountViewSet, SpecialOfferViewSet)
# from cart.views import CartAPI

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
    # path('api/v1/cart/', CartAPI.as_view(), name='cart'),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
