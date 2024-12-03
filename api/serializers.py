from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        depth = 1


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(many=False, read_only=True)
    class Meta:
        model = Student
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    class Meta:
        model = Enrollment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    evaluations = EvaluationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1


class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = '__all__'


class CurriculumSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Curriculum
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    courses = CourseScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 1


class ClassroomSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
            'date_joined': {'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Email is already registered')
        return value

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_teacher(self, obj):
        try:
            teacher = Teacher.objects.get(user=obj)
            return teacher.id_teacher
        except Teacher.DoesNotExist:
            return None

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.groups.add(Group.objects.get(name='Teacher'))
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
