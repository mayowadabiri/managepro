from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)

    class Meta:
        model = Service
        read_only_fields = ("id", "created_at", "added_by")
        fields = ('name', "image_url") + read_only_fields

    def create(self, validated_data):
        validated_data["added_by"] = self.context["request"].user
        return super().create(validated_data)
