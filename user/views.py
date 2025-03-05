from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token

from managepro.utils import api_response

from .serializer import UserSerializer
from .models import User, Code
from .schema import VerificationType


# Create your views here.


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.generate_verification_code()
            return Response({
                "message": "User created Successfully",
            }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeVerificationView(APIView):
    permission_classes = [AllowAny]

    class Incoming(serializers.Serializer):
        code = serializers.CharField(max_length=6)
        email = serializers.EmailField()
        verification_type = serializers.ChoiceField(
            choices=[(tag.value, tag.name) for tag in VerificationType]
        )

    def post(self, request):
        bad_status = status.HTTP_400_BAD_REQUEST
        serializer = self.Incoming(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            verification_type = serializer.validated_data.get(
                "verification_type")

            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"errors": "User does not exist"}, status=bad_status)
            verification_code = serializer.validated_data.get("code")
            code = user.code.filter(
                verification_type=verification_type, verification_code=verification_code).first()
            if not code:
                return Response({"errors": "Invalid verification code."}, status=bad_status)
            expires_at = code.expires_at

            if expires_at < timezone.now():
                user.generate_verification_code()
                return Response({"errors": "Verification code has expired. A new code has been sent to your email address"}, status=bad_status)

            if verification_type == VerificationType.REGISTER.value:
                user.is_verified = True
                user.save()
            code.consumed_at = timezone.now()
            code.save()
            return api_response(message="User verification successfull")


class LoginView(APIView):
    permission_classes = [AllowAny]

    class Incoming(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=16)

    def post(self, request):
        srlz = self.Incoming(data=request.data)
        if srlz.is_valid():
            email = srlz.validated_data.get("email")
            password = srlz.validated_data.get("password")
            user = authenticate(username=email, password=password)

            if not user:
                return Response({"errors": "You have entered wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                return Response({"errors": "User has not been verified"}, status=status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)
            response = api_response(
                message="Login Successful", data={"token": token.key})
            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                secure=True,
                samesite="Strict",
                expires=datetime.utcnow() + timedelta(days=365)
            )
            return response


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    class Incoming(serializers.Serializer):
        email = serializers.EmailField(required=True)

    def post(self, request):
        srlz = self.Incoming(data=request.data)
        if srlz.is_valid():
            email = srlz.validated_data.get('email')
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({"errors": "A mail has been sent to the email address provided"}, status=status.HTTP_400_BAD_REQUEST)

            valid_code = user.code.filter(
                verification_type=VerificationType.FORGOT_PASSWORD.value, consumed_at__isnull=True).first()
            code = valid_code
            if not valid_code:
                code = valid_code = user.generate_verification_code(
                    type=VerificationType.FORGOT_PASSWORD.value)
            elif valid_code.expires_at < timezone.now():
                valid_code.delete()
                code = user.generate_verification_code(
                    verification_type=VerificationType.FORGOT_PASSWORD.value)
            print(code)
            return api_response(message="A mail has been sent to the email address provide")


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    class Incoming(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(max_length=30, required=True)

    def post(self, request):
        srlz = self.Incoming(data=request.data)
        if srlz.is_valid():
            email = srlz.validated_data.get("email")
            password = srlz.validated_data.get("password")
            user = User.objects.filter(email=email).first()
            valid_code = Code.objects.filter(
                user=user, verification_type=VerificationType.FORGOT_PASSWORD.value, consumed_at__isnull=False).first()
            print(valid_code)
            if not valid_code:
                return Response({"error": "Unauthorized request. Verify OTP first."}, status=status.HTTP_403_FORBIDDEN)
            user.set_password(password)
            user.save()
            valid_code.delete()
            return api_response(message="Password changed successfully")
