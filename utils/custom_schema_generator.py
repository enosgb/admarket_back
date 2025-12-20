from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def determine_path_prefix(self, paths):
        """
        Força o prefixo comum a ser vazio.
        Assim as paths aparecem completas no Swagger: /api/v1/users/
        """
        return ""

    def get_operation_keys(self, subpath, method, view):
        keys = super().get_operation_keys(subpath, method, view)
        if len(keys) >= 2 and keys[:2] == ["api", "v1"]:
            return keys[2:]
        return keys
