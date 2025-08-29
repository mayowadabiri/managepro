from rest_framework import serializers

from subscription.models import Subscription

from service.models import Service

from service.serializer import ServiceSerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    is_new = serializers.BooleanField(write_only=True)
    service_id = serializers.CharField(write_only=True)
    service_details = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        read_only_fields = ("id", "uuid", "service_details",  "created_at", "user_id",
                            "created_at")
        fields = ("service_id", "is_free_trial", "free_trial_start_date", "free_trial_billing_cycle",
                  "free_trial_end_date", "billing_cycle", "current_billing_date", "next_billing_date", "status", "currency",
                  "notification_period", "is_new", "amount") + read_only_fields

    def to_internal_value(self, data):
        """
        Overriding the to_internal_value method to handle the service_id field
        """
        validated_data = super().to_internal_value(data)
        service_id = validated_data["service_id"]
        is_new = validated_data["is_new"]
        user = self.context.get("request").user

        if is_new:
            service = Service.objects.create(name=service_id, added_by=user)
            validated_data["service_id"] = service
        else:
            service = Service.objects.get(id=int(service_id))
            validated_data["service_id"] = service
        validated_data["user_id"] = user
        validated_data.pop("is_new")
        return validated_data

    def get_service_details(self, subscription):
        service = ServiceSerializer(subscription.service_id).data
        return service
