from rest_framework import serializers
from accounts.models import User
from .models import *

class StudentRegistrationSerializer(serializers.ModelSerializer):
    name=serializers.CharField(write_only=True)
    email=serializers.EmailField(write_only=True)
    password=serializers.CharField(write_only=True)
    Standard_id=serializers.IntegerField(write_only=True)
    Section_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Student
        fields=['id','name','email','password','Standard_id','Section_id']
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'],
            role='student'
        )
        standard=Standard.objects.get(id=validated_data['Standard_id'])
        section=Section.objects.get(id=validated_data['Section_id'])

        student=Student.objects.create(
            user=user,
            standard=standard,
            section=section
        )
        return student
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.user.first_name,
            'email': instance.user.email,
            'standard': instance.standard.name if instance.standard else None,
            'section': instance.section.name if instance.section else None,
        }
class LinkParentSerializer(serializers.ModelSerializer):
    parent_id=serializers.IntegerField()
    student_id=serializers.IntegerField()

    class Meta:
        model=ParentStudent
        fields=['id','parent_id','student_id']

    def validate(self,data):
        try:
            parent=User.objects.get(id=data['parent_id'],role='parent')
        except User.DoesNotExist:
            raise serializers.ValidationError("Parent with this ID does not exist or is not a parent.")
        try:
            student=Student.objects.get(id=data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student with this ID does not exist.")
        return data
    def create(self, validated_data):
        parent=User.objects.get(id=validated_data['parent_id'],role='parent')
        student=Student.objects.get(id=validated_data['student_id'])
        link=ParentStudent.objects.create(
            parent=parent,
            student=student
        )
        return link
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'parent': {
                'id': instance.parent.id,
                'name': instance.parent.name,
                'email': instance.parent.email,
            },
            'student': {
                'id': instance.student.id,
                'name': instance.student.user.name,
                'email': instance.student.user.email,
            }
        }
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=['id','Sectionname']
class StandardSerializer(serializers.ModelSerializer):
    sections=SectionSerializer(many=True,read_only=True)
    class Meta:
        model=Standard
        fields=['id','standardname','sections']
class AttendanceSerializer(serializers.ModelSerializer):
    student_id=serializers.IntegerField()
    date=serializers.DateField()
    status=serializers.ChoiceField(choices=[('present', 'Present'), ('absent', 'Absent')])
    class Meta:
        model=Attendance
        fields=['id','student_id','date','status']  
  