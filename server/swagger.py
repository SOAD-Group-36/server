from collections import OrderedDict

from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import no_body
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class ReadOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.write_only:
                new_fields[fieldName] = field
        return new_fields


class WriteOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.read_only:
                new_fields[fieldName] = field
        return new_fields


class BlankMeta:
    pass


class ReadWriteAutoSchema(SwaggerAutoSchema):
    def get_view_serializer(self):
        return self._convert_serializer(WriteOnly)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self._convert_serializer(ReadOnly)

    def _convert_serializer(self, new_class):
        serializer = super().get_view_serializer()
        if not serializer:
            return serializer

        class CustomSerializer(new_class, serializer.__class__):
            class Meta(getattr(serializer.__class__, "Meta", BlankMeta)):
                ref_name = new_class.__name__ + serializer.__class__.__name__

        new_serializer = CustomSerializer(data=serializer.data)
        return new_serializer


schema_view = get_schema_view(
    openapi.Info(
        title="Local Marketplace",
        default_version="v1.0.0",
        description="This is set of API's for business to integrate our services in their applications.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="abcd@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_urls = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
