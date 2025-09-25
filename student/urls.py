from django.urls import path
from .views import StudentRegistrationView,LinkParenttoStudentView,StandardListCreateView,SectionListCreateView
urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('link-parent/', LinkParenttoStudentView.as_view(), name='link-parent-student'),
    path('standards/', StandardListCreateView.as_view(), name='standard-list-create'),
    path('sections/', SectionListCreateView.as_view(), name='section-list-create'),
]
