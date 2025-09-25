from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('create-user/', Createteacherparentview.as_view(), name='create-user'),
    path('login/', csrf_exempt(SessionLoginView.as_view()), name='login'),
    path('logout/', csrf_exempt(SessionLogoutView.as_view()), name='logout'),   
    path('reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm')
]