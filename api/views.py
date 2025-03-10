from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Sum

from subscription.models import Subscription


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    cycle = request.query_params.get('cycle', "monthly")
    print(cycle)
    amount = Subscription.objects.filter(
        user_id=request.user, billing_cycle=cycle).aggregate(total=Sum("amount"))["total"]

    return Response({"total_expenses": amount})
