
from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token


from .serializer import UserSerializer
from .models import User
from managepro.utils import api_response

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


class TokenVerificationView(APIView):
    permission_classes = [AllowAny]

    class Incoming(serializers.Serializer):
        code = serializers.CharField(max_length=6)
        email = serializers.EmailField()

    def post(self, request):
        bad_status = status.HTTP_400_BAD_REQUEST
        serializer = self.Incoming(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"errors": "User does not exist"}, status=bad_status)
            if user.is_verified:
                return Response({"errors": "User has already been verified. Please login"}, status=bad_status)
            verification_code = serializer.validated_data.get("code")
            expires_at = user.verification_code_expires_at
            is_valid_code = int(verification_code) == int(
                user.verification_code)

            if not is_valid_code:
                return Response({"errors": "Invalid verification code."}, status=bad_status)

            if expires_at < timezone.now():
                user.generate_verification_code()
                return Response({"errors": "Verification code has expired. A new code has been sent to your email address"}, status=bad_status)

            user.is_verified = True
            user.verification_code = None
            user.verification_code_expires_at = None
            user.save()
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
            return api_response(message="Login Successful", data={"token": token.key})
