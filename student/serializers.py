from rest_framework import serializers
from accounts.models import User
from .models import Student,Standard,Section

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
            name=validated_data['name'],
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
            'name': instance.user.name,
            'email': instance.user.email,
            'standard': instance.standard.name if instance.standard else None,
            'section': instance.section.name if instance.section else None,
        }