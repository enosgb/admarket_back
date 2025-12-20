from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer

from .serializers import LoginRequestSerializer
from .swagger_schemas import login_schema


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @login_schema
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return Response({"detail": "Credenciais inválidas"}, status=401)
        login(request, user)
        return Response(
            {"detail": "Login realizado", "user": UserSerializer(user).data}
        )


class LogoutView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logout realizado"})
