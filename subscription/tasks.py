from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils.timezone import localdate, now, timedelta

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer

logger = get_task_logger(__name__)


@shared_task
def update_free_trial_details():
    today = now()
    next_day = today + timedelta(days=1)
    qs = Subscription.objects.filter(
        is_free_trial=True,
        free_trial_end_date__gte=next_day,
        free_trial_end_date__lte=next_day).select_related("user_id")

    subscriptions = SubscriptionSerializer(qs, many=True).data

    for subcription in subscriptions:
        print(subcription)
    print("Updating User Free Trial")


@shared_task
def update_next_billing_cyle():
    print("Updating Next Billing Cycle")


@shared_task
def update_to_expire():
    print("Updating To Expire Notification")
