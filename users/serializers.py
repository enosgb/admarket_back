from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "image",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("O email é obrigatório")
        return value.lower()

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
