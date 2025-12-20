from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_yasg_schema_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from utils.custom_schema_generator import CustomSchemaGenerator

schema_view = get_yasg_schema_view(
    openapi.Info(
        title="Ad Maker",
        default_version="v0",
        description="Docs Ad Maker API REST",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="enosgb55@gmail.com"),
        license=openapi.License(name="Licença MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomSchemaGenerator,
)


class RootView(APIView):
    """
    Exibe uma lista de rotas disponíveis.
    """

    def get(self, request, *args, **kwargs):
        routes = {}
        return Response(routes)


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Docs
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/", RootView.as_view(), name="root"),
]
