from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import CreateUserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.
class Createteacherparentview(CreateAPIView):
   
    serializer_class = CreateUserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
         return super().post(request, *args, **kwargs)
