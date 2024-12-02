from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, 'students')
router.register(r'attendances', AttendanceViewSet, 'attendances')
router.register(r'classrooms', ClassroomViewSet, 'classrooms')
router.register(r'curriculums', CurriculumViewSet, 'curriculums')
router.register(r'courses', CourseViewSet, 'courses')
router.register(r'evaluations', EvaluationViewSet, 'evaluations')
router.register(r'schedules', ScheduleViewSet, 'schedules')
router.register(r'course-schedules', CourseScheduleViewSet, 'course-schedules')
router.register(r'subjects', SubjectViewSet, 'subjects')
router.register(r'enrollments', EnrollmentViewSet, 'enrollments')
router.register(r'parents', ParentViewSet, 'parents')
router.register(r'teachers', TeacherViewSet, 'teachers')
router.register(r'users', UserViewSet, 'users')



urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]

