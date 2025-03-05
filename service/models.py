from django.db import models
from uuid import uuid4


from user.models import User
# Create your models here.


class Service(models.Model):

    name = models.CharField(max_length=100)

    image_url = models.URLField(blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    domain = models.URLField(null=True, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
