from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .views import swagger_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('code_review.urls')),
    path('', views.index_view),

    # Swagger APIs

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', swagger_schema_view().without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', swagger_schema_view().with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', swagger_schema_view().with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
