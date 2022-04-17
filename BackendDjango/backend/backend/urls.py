from django.contrib import admin
from django.urls import path, include, re_path
# swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="project A title", # 타이틀
        default_version='v1', # 버전
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # swagger
    re_path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]

from api.dataControl import gameListsDumping, userSteamDataDumping, userDataDumping


gameListsDumping()
userSteamDataDumping()
userDataDumping()