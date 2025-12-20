from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email", required=True)
    password = serializers.CharField(help_text="Senha", required=True)
