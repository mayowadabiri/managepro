from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=16, required=True, write_only=True)

    class Meta:
        model = User
        read_only_fields = ("id", "uuid", "is_active",
                            "is_verified")
        fields = read_only_fields + (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password"
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
