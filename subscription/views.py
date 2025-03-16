from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from subscription.serializers import SubscriptionSerializer
from subscription.models import Subscription

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


from subscription.schema import Status, Cycle


class SubscriptionFilter(filters.FilterSet):

    name = filters.CharFilter(
        field_name="service_id__name", lookup_expr='icontains')
    amount_gte = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    amount_lte = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    status = filters.ChoiceFilter(
        choices=[(choice.value, choice.name) for choice in Status])
    cycle = filters.ChoiceFilter(
        choices=[(cycle.value, cycle.name) for cycle in Cycle])

    class Meta:
        model = Subscription
        fields = []


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscriptionFilter
    queryset = Subscription.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().filter(
            user_id=self.request.user).select_related("service_id")
        return qs
