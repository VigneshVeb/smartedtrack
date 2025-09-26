from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Student
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class isTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'
class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [isTeacher]
class LinkParenttoStudentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [isTeacher]
class StandardListCreateView(generics.ListCreateAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = [isTeacher]
class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes =[isTeacher]
class AttendanceMarkView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, isTeacher]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)

        records = []

        # Case: Bulk Attendance
        if isinstance(serializer.validated_data, list):
            for item in serializer.validated_data:
                student_id = int(item["student_id"])
                date = item["date"]
                status_ = item["status"]

                attendance = Attendance.objects.filter(
                    student_id=student_id, date=date
                ).first()

                if attendance:
                    attendance.status = status_
                    attendance.marked_by = request.user
                    attendance.save()
                else:
                    attendance = Attendance.objects.create(
                        student_id=student_id,
                        date=date,
                        status=status_,   # ✅ fixed variable
                        marked_by=request.user
                    )

                records.append(attendance)  # ✅ use attendance not obj

        # Case: Single Attendance
        else:
            obj, created = Attendance.objects.update_or_create(
                student_id=serializer.validated_data['student_id'],
                date=serializer.validated_data['date'],
                defaults={
                    'status': serializer.validated_data['status'],
                    'marked_by': request.user
                }
            )
            records.append(obj)

        return Response(
            AttendanceSerializer(records, many=True).data,
            status=status.HTTP_200_OK  # ✅ fixed typo
        )
    
