from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)

    class Meta:
        model = Service
        read_only_fields = ("id", "created_at")
        fields = ('name', "image_url") + read_only_fields
