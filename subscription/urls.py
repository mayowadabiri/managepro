
from rest_framework.routers import DefaultRouter

from subscription.views import SubscriptionViewSet


router = DefaultRouter(trailing_slash=False)

router.register(r"", SubscriptionViewSet, basename="subscription")
urlpatterns = router.urls
