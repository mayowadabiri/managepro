
from rest_framework.routers import DefaultRouter

from .views import ServiceViewset


router = DefaultRouter(trailing_slash=False)

router.register(r"", ServiceViewset, basename="services")
urlpatterns = router.urls
