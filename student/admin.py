from django.contrib import admin
from .models import Standard, Section, Student
# Register your models here.
@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','standardname']
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id','Sectionname','standard']
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','standard','section','created_at']