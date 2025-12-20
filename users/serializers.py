from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "image",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]
