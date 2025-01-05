from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.swagger.generator import BothHttpAndHttpsSchemaGenerator

main_schema_view = get_schema_view(
    openapi.Info(
        title="Clinic CRM API",
        default_version="v1",
        description="This Documentation shows list of api and will give chance to check them",
        contact=openapi.Contact(email="cbekoder@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)
