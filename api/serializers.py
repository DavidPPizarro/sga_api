from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class SubjectSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1
    def create(self, validated_data):
        course = validated_data.pop('course')
        teacher = validated_data.pop('teacher')
        subject = Subject.objects.create(course=course, teacher=teacher, **validated_data)
        return subject

class EvaluationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())    
    class Meta:
        model = Evaluation
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        student = validated_data.pop('student')
        course = validated_data.pop('course')
        evaluation = Evaluation.objects.create(student=student, course=course, **validated_data)
        return evaluation

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1
        
    def create(self, validated_data):     
        student = validated_data.pop('student')
        course = validated_data.pop('course')
        attendance = Attendance.objects.create(student=student, course=course, **validated_data)
        return attendance

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Parent.objects.all(),
        write_only=True
    )
    parent_details = ParentSerializer(source='parent', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        
    def create(self, validated_data):
        parent = validated_data.pop('parent')
        student = Student.objects.create(parent=parent, **validated_data)
        return student


class EnrollmentSerializer(serializers.ModelSerializer):    
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True
    )
    curriculum = serializers.PrimaryKeyRelatedField(queryset=Curriculum.objects.all())    
    student_details = StudentSerializer(source='student', read_only=True)
    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        required=False
    )
        
    class Meta:
        model = Enrollment
        fields = '__all__'

    def create(self, validated_data):
        student = validated_data.pop('student')
        curriculum = validated_data.pop('curriculum')
        courses = validated_data.pop('courses', [])
        
        # First create the enrollment
        enrollment = Enrollment.objects.create(
            student=student, 
            curriculum=curriculum, 
            **validated_data
        )
        
        # Then add the courses
        for course in courses:
            enrollment.courses.add(course)
            
        return enrollment

class CourseSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    evaluations = EvaluationSerializer(many=True, read_only=True)
    curriculum = serializers.PrimaryKeyRelatedField(queryset=Curriculum.objects.all())
    
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        curriculum = validated_data.pop('curriculum')
        course = Course.objects.create(curriculum=curriculum, **validated_data)
        return course


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


# Primero, define un serializer base para evitar la dependencia circular
class ClassroomBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())    
    classroom_details = ClassroomBaseSerializer(source='classroom', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        classroom = validated_data.pop('classroom')
        schedule = Schedule.objects.create(classroom=classroom, **validated_data)
        return schedule

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
