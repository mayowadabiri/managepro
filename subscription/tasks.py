from celery import shared_task
from celery.utils.log import get_task_logger
from django.forms.models import model_to_dict

from django.utils.timezone import now, timedelta, localdate

from subscription.models import Subscription
from subscription.schema import Status

logger = get_task_logger(__name__)


# def get_weekly_range(today):
#     """Returns the start (Sunday) and end (Saturday) of the current week."""
#     days_since_sunday = today.weekday() + 1  # Convert Monday (0) to Sunday (0)
#     start_of_week = today - timedelta(days=days_since_sunday % 7)
#     days_until_saturday = (5 - today.weekday()) % 7
#     end_of_week = today + timedelta(days=days_until_saturday)
#     return start_of_week, end_of_week


@shared_task
def update_free_trial_details():
    today = now()
    next_day = today + timedelta(days=1)
    qs = Subscription.objects.filter(
        is_free_trial=True,
        free_trial_end_date__gte=next_day,
        free_trial_end_date__lte=next_day).select_related("user_id")

    for subscription in qs:
        # Send email/push notification to user
        subscription.is_free_trial = False
        subscription.save()
    print("Updating User Free Trial")


@shared_task
def update_next_billing_cyle():
    print("Updating Next Billing Cycle")


@shared_task
def send_one_week_notification():
    '''
        Runs everyday to send notification to subscriptions
        that will be expiring in a week from expiry date
    '''
    today = localdate(now())
    # start_date, end_date = get_weekly_range(today)
    qs = Subscription.objects.filter(status=Status.ACTIVE.value)

    today = localdate(now())

    for subscription in qs:
        next_billing_date = subscription.next_billing_date

        difference = next_billing_date - today

        if difference.days == 7:
            # Send email/push notification to user
            subscription.status = Status.TOEXPIRE.value
            subscription.save()


@shared_task
def three_days_notification():
    '''
         Runs everyday to send notification to subscriptions
         that will be expiring in 3 days from expiry date
     '''


print("Updating To Expire Notification")


@shared_task
def one_day_notification():
    '''
         Runs everyday to send notification to subscriptions
         that will be expiring in 24 hours from expiry date
     '''


print("Updating To Expire Notification")
