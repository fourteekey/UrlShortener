from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from shortener.views import index_page

schema_view = get_schema_view(
    openapi.Info(
        title="UrlShortener",
        default_version='v1',
    ),
    url=settings.API_URL
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # http://127.0.0.1:8000/api/v1/
    path('api/v1/', include('api.api')),

    # http://127.0.0.1:8000/
    re_path('.*', index_page, name='index'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
