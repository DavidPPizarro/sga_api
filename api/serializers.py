from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'
        depth = 1


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'


class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'
        depth = 1

class AlumnoSerializer(serializers.ModelSerializer):
    evaluaciones = EvaluacionSerializer(many=True, read_only=True)
    class Meta:
        model = Alumno
        fields = '__all__'
        depth = 1

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'
        depth = 1

class CursoSerializer(serializers.ModelSerializer):
    asistencias = AsistenciaSerializer(many=True, read_only=True)
    evaluaciones = EvaluacionSerializer(many=True, read_only=True)
    class Meta:
        model = Curso
        fields = '__all__'

class RepresentanteSerializer(serializers.ModelSerializer):
    alumnos = AlumnoSerializer(many=True, read_only=True)
    class Meta:
        model = Representante
        fields = '__all__'




class Curso_MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Matricula
        fields = '__all__'
        depth = 1


class CurriculoSerializer(serializers.ModelSerializer):
    cursos = CursoSerializer(many=True, read_only=True)

    class Meta:
        model = Curriculo
        fields = '__all__'


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'


class Horario_CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario_Curso
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

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
            raise ValidationError('The email address is already registered')
        return value

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

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
    materias = MateriaSerializer(many=True, read_only=True)
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = '__all__'
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.groups.add(Group.objects.get(id=3))
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
