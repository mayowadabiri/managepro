from django.db import models

from uuid import uuid4

from user.models import User

from .schema import Cycle, Status, Currency
# Create your models here.


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscription")

    is_free_trial = models.BooleanField(default=False)

    free_trial_start_date = models.DateTimeField()

    free_trial_billing_cycle = models.CharField(
        (cycle.value, cycle.name) for cycle in Cycle)

    free_trial_end_date = models.DateTimeField()

    billing_cycle = models.CharField(
        (cycle.value, cycle.name) for cycle in Cycle)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField((status.value, status.name) for status in Status)

    currency = models.CharField((currency.value, currency.name)
                                for currency in Currency)

    notification_period = models.IntegerField()

    # uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
