from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Sum
from django.utils.timezone import now, localdate, timedelta

from subscription.models import Subscription
from subscription.schema import Cycle, Status

import calendar


def get_monthly_range(today):
    """Returns the first and last day of the current month"""
    start_of_month = today.replace(day=1)
    _, last_day = calendar.monthrange(today.year, today.month)
    end_of_month = today.replace(day=last_day)
    return start_of_month, end_of_month


def get_subscription_data(start_date, end_date, today):
    user_subscription = Subscription.objects.filter(
        next_billing_date__gte=start_date, next_billing_date__lte=end_date)

    current_subscription = user_subscription.filter(
        next_billing_date__gte=today)

    total_expenses = user_subscription.aggregate(
        total=Sum("amount"))["total"]

    remaining_expenses = current_subscription.aggregate(
        total=Sum("amount"))["total"]

    outstanding_subscription = current_subscription.count()

    active_subscription = user_subscription.filter(
        status=Status.ACTIVE.value).count()

    to_expire_subscription = user_subscription.filter(
        status=Status.TOEXPIRE.value).count()

    return {"total_expenses": total_expenses,
            "outstanding_subscription": outstanding_subscription,
            "active_subscription": active_subscription,
            "to_expire_subscription": to_expire_subscription, "remaining_expenses": remaining_expenses}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    """
    Get dashboard data. Total expenses, Outstanding Subscription, Active Subscription and Subscription about to expire
    This is based on a periodic basis -  Weekly, Monthly and Yearly
    """
    cycle = request.query_params.get('cycle', "monthly")
    today = localdate(now())
    if cycle == Cycle.MONTHLY.value:
        start_date, end_date = get_monthly_range(today)
        print(start_date, end_date)

    subscription_data = get_subscription_data(start_date, end_date, today)
    return Response(subscription_data)
