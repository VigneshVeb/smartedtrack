from django.urls import path
from .views import *
urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('link-parent/', LinkParenttoStudentView.as_view(), name='link-parent-student'),
    path('standards/', StandardListCreateView.as_view(), name='standard-list-create'),
    path('sections/', SectionListCreateView.as_view(), name='section-list-create'),
    path('mark-attendance/', AttendanceMarkView.as_view(), name='mark-attendance'),
 path("attendance/student/<int:student_id>/",StudentAttendanceView.as_view(), name="student-attendance"),
 path("attendance/class/<int:section_id>/",ClassAttendanceView.as_view(), name="create-attendance-for-class"),
 path("attendance/report/", AttendanceReportPrincipleView.as_view(), name="attendance-report"),
 path("attendance/teacher/<int:teacher_id>/",AttendanceReportParentView.as_view(), name="teacher-attendance"),

]

