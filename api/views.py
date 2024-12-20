from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django_filters import rest_framework as django_filters

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({'email': str(e)})

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            return Response({"message": "Successful login", "user": UserSerializer(user).data}, status=200)
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=400)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseFilter(django_filters.FilterSet):
    school_year = django_filters.NumberFilter(field_name='school_year')
    curriculum = django_filters.NumberFilter(field_name='curriculum__id_curriculum')
    
    class Meta:
        model = Course
        fields = ['school_year', 'curriculum']
        

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = CourseFilter

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(courses__id_course=self.kwargs['course_pk'])


class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class AutoEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = AutoEnrollmentSerializer