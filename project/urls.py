from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="HOUM API V1",
        default_version='v1',
        description="Backend developer test by jaisir",
        contact=openapi.Contact(email="jaisirenterprise@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('api/v1/houm/', include('apps.houmers.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'apps.utils.errors.error_400'
handler403 = 'apps.utils.errors.error_403'
handler404 = 'apps.utils.errors.error_404'
handler500 = 'apps.utils.errors.error_500'
