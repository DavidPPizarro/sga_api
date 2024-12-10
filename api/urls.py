from django.urls import path, include

from rest_framework_nested import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import *

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'attendances', AttendanceViewSet, 'attendances')
router.register(r'classrooms', ClassroomViewSet, 'classrooms')
router.register(r'curriculums', CurriculumViewSet, 'curriculums')
router.register(r'evaluations', EvaluationViewSet, 'evaluations')
router.register(r'schedules', ScheduleViewSet, 'schedules')
router.register(r'course-schedules', CourseScheduleViewSet, 'course-schedules')
router.register(r'subjects', SubjectViewSet, 'subjects')
router.register(r'parents', ParentViewSet, 'parents')
router.register(r'teachers', TeacherViewSet, 'teachers')
router.register(r'users', UserViewSet, 'users')
router.register(r'enrollments', AutoEnrollmentViewSet, 'enrollments')

courses_router = NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'enrollments', EnrollmentViewSet, basename='course-enrollments')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(courses_router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]

