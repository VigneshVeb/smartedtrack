from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Teacher
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializer import TeacherSerializer


# Create your views here.
class Createteacherstudent(CreateAPIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            queryset = Teacher.objects.all()
            serializer_class = TeacherSerializer
            return super().post(request, *args, **kwargs)
           
            
 
