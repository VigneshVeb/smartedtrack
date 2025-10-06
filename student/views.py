from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Student
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import json


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
    permission_classes = []  # or IsAuthenticated

    def post(self, request, *args, **kwargs):
        py_data = request.data  # already a dict or list
        many = isinstance(py_data, list)
        serializer = self.get_serializer(data=py_data, many=many)
        serializer.is_valid(raise_exception=True)

        records = []
        teacher = User.objects.get(id=24)
        # Case: Bulk Attendance
        if many:
            for item in serializer.validated_data:
                student_id = int(item["student_id"])
                date = item["date"]
                status_ = item["status"]
                
                attendance = Attendance.objects.filter(
                    student_id=student_id, date=date
                ).first()

                if attendance:
                    attendance.status = status_
                    attendance.marked_by = teacher
                    attendance.save()
                else:
                    attendance = Attendance.objects.create(
                        student_id=student_id,
                        date=date,
                        status=status_,
                        marked_by=teacher
                    )

                records.append(attendance)

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
            status=status.HTTP_200_OK
        )

class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("🔍 CSRF Token from request:", self.request.META.get('HTTP_X_CSRFTOKEN'))
        print("🔍 Session ID:", self.request.COOKIES.get('sessionid'))
        student_id = self.kwargs['student_id']
        if self.request.user.role == 'student' and self.request.user.id == int(student_id):
            return Attendance.objects.none()
        return Attendance.objects.filter(student_id=student_id).order_by('-date')
class ClassAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated,isTeacher]
    def get_queryset(self):
        section_id = self.kwargs['section_id']
        section = Section.objects.get(id=section_id)
        date = self.request.query_params.get('date')
        user_ids = [student.user.id for student in Student.objects.filter(section=section)]
        students = User.objects.filter(id__in=user_ids, role='student')
        if date:
            return Attendance.objects.filter(student__in=students, date=date)
        return Attendance.objects.filter(student__in=students).order_by('-date')
    def calculate_percentage(self, present_days, total_days):
        if total_days == 0:
            return 0.0
        return f"{round((present_days / total_days) * 100,2)}%"
class AttendanceReportPrincipleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def calculate_percentage(self, present_days, total_days):
        if total_days == 0:
            return "0.0%"
        return f"{round((present_days / total_days) * 100, 2)}%"

    def get(self, request, *args, **kwargs):
        queryset = Attendance.objects.all()
        standard_name = request.query_params.get('standard')
        section_name = request.query_params.get('section')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Always initialize
        user_ids = None  

        if standard_name:
            std = Standard.objects.get(name=standard_name)
            students = Student.objects.filter(standard=std)
            user_ids = [student.user.id for student in students]
            queryset = queryset.filter(student_id__in=user_ids)


        if section_name:
            sec = Section.objects.get(name=section_name)
            students = Student.objects.filter(section=sec)
            user_ids = [student.user.id for student in students]
            queryset = queryset.filter(student_id__in=user_ids)


        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        summary_data = []
        student_ids = queryset.values_list('student_id', flat=True).distinct()

        for sid in student_ids:
            student_records = queryset.filter(student_id=sid)
            if not student_records.exists():
                continue
            student = student_records.first().student
            user = student_records.first().student
            total_days = student_records.count()
            present_days = student_records.filter(status='present').count()
            absent_days = student_records.filter(status='absent').count()
            

            summary_data.append({
                'student_id': student.id,
        'student_name': f"{student.user.first_name} {student.user.last_name}",
        'standard': student.standard.standardname if student.standard else "",
        'section': student.section.Sectionname if student.section else "",
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'attendance_percentage': self.calculate_percentage(present_days, total_days),
    })
        

        total_students = len(student_ids)
        total_days = queryset.values('date').distinct().count()
        overall_present = queryset.filter(status='present').count()
        overall_percentage = self.calculate_percentage(overall_present, queryset.count())

        return Response({
            "summary": {
                "total_students": total_students,
                "total_days": total_days,
                "overall_attendance_percentage": overall_percentage,
            },
            "records": summary_data,
        })

class AttendanceReportParentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def calculate_percentage(self, present_days, total_days):
        if total_days == 0:
            return "0.0%"
        return f"{round((present_days / total_days) * 100, 2)}%"

    def get(self, request, *args, **kwargs):
        parent = request.user
        linked_students = [ps.student for ps in ParentStudent.objects.filter(parent=parent)]

        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        data = []
        for sid in linked_students:
            student_records = Attendance.objects.filter(student_id=sid)
            if from_date and to_date:
                student_records = student_records.filter(date__range=[from_date, to_date])

            if not student_records.exists():
                continue

            student = student_records.first().student
            total_days = student_records.count()
            present_days = student_records.filter(status='present').count()
            absent_days = student_records.filter(status='absent').count()
            child_data = {
                "student_name":student.user.full_name,
                "standard": student.standard.standardname,
                "section": student.section.Sectionname,
                "summary":{
                    "total_days": total_days,
                    "present_days": present_days,
                    "absent_days": absent_days,
                    "attendance_percentage": self.calculate_percentage(present_days, total_days),
                },
                "records": AttendanceDailySerializer(student_records, many=True).data
            }
            data.append(child_data) 
        return Response({"children":data})





         
