from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Teacher(models.Model):
    id_teacher = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher')
    specialty = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Parent(models.Model):
    id_parent = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    id_student = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, default='', unique=True)
    birth_date = models.DateField()
    enrollment_date = models.DateField()
    address = models.CharField(max_length=100, default='Unknown')
    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Curriculum(models.Model):
    id_curriculum = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='inactive')
    school_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"


class Course(models.Model):
    id_course = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    weekly_hours = models.IntegerField()
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name


class Classroom(models.Model):
    id_classroom = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    id_enrollment = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active')
    courses =models.ManyToManyField(Course, related_name='enrollments')

    def __str__(self):
        return f"Enrollment of {self.student}"


class Evaluation(models.Model):
    id_evaluation = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='evaluations')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='evaluations')
    TYPE_CHOICES = [
        ('continuous', 'Continuous'),
        ('partial 1', 'Partial 1'),
        ('partial 2', 'Partial 2'),
        ('partial 3', 'Partial 3'),
        ('final', 'Final'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    grade = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation of {self.student} in {self.course}"


class Attendance(models.Model):
    id_attendance = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    STATUS_CHOICES = [
        ('attended', 'Attended'),
        ('not attended', 'Not Attended'),
    ]
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='not attended')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='attendances')

    def __str__(self):
        return f"Attendance of {self.student} - {self.date}"


class Schedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    day = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name='schedules')

    def __str__(self):
        return f"Schedule {self.id_schedule}: {self.day} from {self.start_time} to {self.end_time}"


class CourseSchedule(models.Model):
    id_course_schedule = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='schedules')
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"CourseSchedule {self.id_course_schedule}: Course {self.course.id_course} - Schedule {self.schedule.id_schedule}"
