from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


schema_view = get_schema_view(
    openapi.Info(title="E-Commerce API", default_version='v1'),
    public=True,
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/',include('apps.accounts.api.urls', namespace='accounts')),
    path('api/v1/products/', include('apps.products.api.urls', namespace='product')),
    path('api/v1/reviews/', include('apps.reviews.api.urls', namespace='reviews')),
    path('api/v1/cart/', include('apps.cart.api.urls', namespace='cart')),
    path('api/v1/order/', include('apps.order.api.urls', namespace='order')),
    path('api/v1/assistant/', include('apps.assistant.api.urls', namespace='chat')),
    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
        ),
    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'api/v1/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),




]+ debug_toolbar_urls()




if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
