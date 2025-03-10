from django.db import models

from uuid import uuid4

from user.models import User
from service.models import Service


from subscription.schema import Cycle, Status, Currency


class Subscription(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="subscription", null=True)

    service_id = models.ForeignKey(
        Service, on_delete=models.SET_NULL, related_name="subscription", null=True)

    is_free_trial = models.BooleanField(default=False)

    free_trial_start_date = models.DateField(null=True)

    free_trial_billing_cycle = models.CharField(
        ((cycle.value, cycle.name) for cycle in Cycle), null=True)

    free_trial_end_date = models.DateField(null=True)

    billing_cycle = models.CharField(
        (cycle.value, cycle.name) for cycle in Cycle)

    current_billing_date = models.DateField()
    next_billing_date = models.DateField()
    status = models.CharField((status.value, status.name) for status in Status)

    currency = models.CharField((currency.value, currency.name)
                                for currency in Currency)

    notification_period = models.IntegerField()

    amount = models.DecimalField(decimal_places=2, max_digits=10)

    uuid = models.UUIDField(default=uuid4,
                            editable=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
