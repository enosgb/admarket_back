from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_operation_keys(self, subpath, method, view):
        keys = super().get_operation_keys(subpath, method, view)

        if keys and keys[0] == 'api':
            keys = keys[1:]

        if len(keys) >= 2:
            keys = [f"{keys[0]} - {keys[1]}"] + keys[2:]
        elif len(keys) == 1:
            keys = [keys[0]]
        else:
            keys = ['default']

        return keys
