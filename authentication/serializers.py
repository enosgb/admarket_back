from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email", required=True)
    password = serializers.CharField(help_text="Senha", required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha antiga está incorreta.")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"new_password": "As novas senhas não coincidem."}
            )
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
