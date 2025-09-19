from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Student
from .serializers import StudentRegistrationSerializer


# Create your views here.
class isTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'
class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [isTeacher]