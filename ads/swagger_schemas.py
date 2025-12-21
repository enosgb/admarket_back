from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProductImageCreateSerializer

products_images_create_schema = swagger_auto_schema(
    request_body=ProductImageCreateSerializer,
    consumes=["multipart/form-data"],
    responses={
        201: ProductImageCreateSerializer,
        400: openapi.Response(
            "Erro",
            examples={"application/json": {"error": "Mensagem de erro"}},
        ),
        403: "Acesso negado",
        404: "Produto não encontrado",
    },
)

products_images_update_schema = swagger_auto_schema(
    request_body=ProductImageCreateSerializer,
    consumes=["multipart/form-data"],
    responses={
        200: ProductImageCreateSerializer,
        400: openapi.Response(
            "Erro",
            examples={"application/json": {"error": "Mensagem de erro"}},
        ),
        403: "Acesso negado",
        404: "Produto não encontrado",
    },
)

