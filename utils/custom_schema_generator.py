# custom_swagger.py
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def determine_path_prefix(self, paths):
        # Remove api/v1 do início da URL
        return ""

    def get_operation_keys(self, subpath, method, view):
        keys = super().get_operation_keys(subpath, method, view)
        # Remove api/v1 e mantém a hierarquia do app
        if len(keys) >= 2 and keys[:2] == ["api", "v1"]:
            keys = keys[2:]
        return keys


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        """
        Gera tags automáticas com hierarquia:
        app > recurso > subrecurso
        """
        if operation_keys is None:
            # fallback: nome da view em snake_case
            operation_keys = self.view.__class__.__name__.lower().split("_")

        # Mantém pelo menos 2 níveis: app > recurso
        if len(operation_keys) >= 2:
            return [
                f"{operation_keys[0].capitalize()} > {operation_keys[1].capitalize()}"
            ]
        elif len(operation_keys) == 1:
            return [operation_keys[0].capitalize()]
        return super().get_tags(operation_keys)
