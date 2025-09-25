from django.db import models
from accounts.models import User

# Create your models here.
class Standard(models.Model):
    standardname = models.CharField(max_length=50)

    def __str__(self):
        return self.standardname
class Section(models.Model):
    Sectionname = models.CharField(max_length=50)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.name} - {self.standard.name}"
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='student_profile')
    standard = models.ForeignKey('Standard', on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class ParentStudent(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')

    def __str__(self):
        return f"{self.parent.username} - {self.student.user.username}"