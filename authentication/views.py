from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer
from utils.send_email import SendEmail

from .serializers import (
    ChangePasswordSerializer,
    LoginRequestSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordSerializer,
)
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


class ResetPasswordRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)

            reset_link = f"{settings.FRONTEND_URL}/reset-password-confirm/?token={token}&email={email}"

            SendEmail(
                "Link de Reset de Senha",
                f"Clique no link para resetar sua senha:\n{reset_link}",
                email,
            ).send()
        except User.DoesNotExist:
            pass

        return Response(
            {
                "detail": "Se o email existir, enviamos instruções para redefinir a senha."
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {"detail": "Token inválido ou expirado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Senha alterada com sucesso."}, status=200)
