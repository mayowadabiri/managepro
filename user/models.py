from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db import models

from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta

from .schema import VerificationType


class UserManager(BaseUserManager):
    """Custom user manager without username requirement."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user using email instead of username."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with elevated permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the unique identifier."""

    username = None
    email = models.EmailField(
        unique=True, error_messages={"unique": "A user with this email address already exists"}
    )
    phone_number = PhoneNumberField(null=False, unique=True, error_messages={
                                    "null": "Please provide a phone number", "unique": "A user with this phone number already exists"})
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid4)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def generate_verification_code(self, type):
        """Generate a 6-digit verification code and set expiry time."""
        code = get_random_string(6, "0123456789")
        expires_at = timezone.now() + timedelta(minutes=15)
        Code.objects.create(
            user=self, verification_code=code, expires_at=expires_at, verification_type=type)
        return code


class Code(models.Model):
    verification_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(null=True)
    verification_type = models.CharField(
        max_length=30,
        choices=[(status.value, status.name) for status in VerificationType],
        default=VerificationType.REGISTER.value
    )
    consumed_at = models.DateTimeField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="code", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.verification_code
