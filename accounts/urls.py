from django.urls import path
from .views import Createteacherparentview
urlpatterns = [
    path('create-user/', Createteacherparentview.as_view(), name='create-user'),
]