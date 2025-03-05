from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication import TokenAuthentication
from .serializer import ServiceSerializer
from .models import Service

# Create your views here.


class ServiceViewset(ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Service.objects.all()
    lookup_field = "pk"
