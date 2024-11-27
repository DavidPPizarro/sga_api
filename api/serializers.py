from rest_framework import serializers
from . import models
from django.core.exceptions import ValidationError

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = '__all__'
        
class RepresentanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Representante
        fields = '__all__'


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alumno
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Matricula
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Curso
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Materia
        fields = '__all__'


class CurriculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Curriculo
        fields = '__all__'


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aula
        fields = '__all__'


class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Evaluacion
        fields = '__all__'


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asistencia
        fields = '__all__'


class Curso_MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Curso_Matricula
        fields = '__all__'


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        fields = '__all__'


class Horario_CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario_Curso
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'groups']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('El correo electrónico ya está registrado')
        return value

    def create(self, validated_data):
        # Crea un usuario con una contraseña encriptada
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
