from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import *
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import passwordresetSerializer,PasswordResetConfirmationSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.middleware.csrf import get_token
# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # disable CSRF check


# 🔒 Create teacher/parent – only logged-in users (admin/teacher) can create
class Createteacherparentview(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = [CsrfExemptSessionAuthentication]


# ✅ Session login – open to everyone (AllowAny)
class SessionLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]  # anyone can log in

    def post(self, request, *args, **kwargs):
        serializer = SessionLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)

            # ✅ Generate and attach CSRF token to the response
            csrf_token = get_token(request)
            response = JsonResponse({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                },
                "csrfToken": csrf_token,  # optional, also send it in JSON for debugging
            })
            response.set_cookie("csrftoken", csrf_token, httponly=False, samesite='Lax')
            return response

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# 🔒 Logout – only logged-in users
class SessionLogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# ✅ Password reset request – open to everyone
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = passwordresetSerializer
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/accounts/reset-password-confirm/?uid={uid}&token={token}"
        return Response(
            {
                "message": "Password reset link has been sent to your email (simulated).",
                "reset_link": reset_link
            },
            status=status.HTTP_200_OK
        )


# ✅ Password reset confirm – open to everyone
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmationSerializer
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)