from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserSerializer

from .serializers import LoginRequestSerializer

login_schema = swagger_auto_schema(
    request_body=LoginRequestSerializer,
    responses={
        200: UserSerializer,
        400: openapi.Response(
            "Erro", examples={"application/json": {"error": "Mensagem de erro"}}
        ),
        403: "Acesso negado",
        404: "Anúncio não encontrado",
    },
)
