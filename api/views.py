from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError

# Importaciones de modelos
from .models import (
    Asistencia, Aula, Curso_Matricula, Evaluacion, Horario, Horario_Curso,
    Representante, Alumno, Curso, Matricula, Curriculo
)

# Importaciones de serializadores
from .serializers import (
    AsistenciaSerializer, AulaSerializer, CurriculoSerializer, Curso_MatriculaSerializer,
    EvaluacionSerializer, Horario_CursoSerializer, HorarioSerializer, RepresentanteSerializer,
    AlumnoSerializer, CursoSerializer, MatriculaSerializer, UserSerializer
)

class CustomPagination(PageNumberPagination):
    page_size = 10

class RepresentanteListCreateView(generics.ListCreateAPIView):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer
    pagination_class = CustomPagination

class AlumnoListCreateView(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    pagination_class = CustomPagination

class CursoListCreateView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    pagination_class = CustomPagination

class MatriculaListCreateView(generics.ListCreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    pagination_class = CustomPagination
    
class CurriculoListCreateView(generics.ListCreateAPIView):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer
    pagination_class = CustomPagination
    
class AulaListCreateView(generics.ListCreateAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    pagination_class = CustomPagination
    
class EvaluacionListCreateView(generics.ListCreateAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    pagination_class = CustomPagination

class AsistenciaListCreateView(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    pagination_class = CustomPagination

class Curso_MatriculaListCreateView(generics.ListCreateAPIView):
    queryset = Curso_Matricula.objects.all()
    serializer_class = Curso_MatriculaSerializer
    pagination_class = CustomPagination

class HorarioListCreateView(generics.ListCreateAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    pagination_class = CustomPagination

class Horario_CursoListCreateView(generics.ListCreateAPIView):
    queryset = Horario_Curso.objects.all()
    serializer_class = Horario_CursoSerializer
    pagination_class = CustomPagination

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    
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
        password = request.data.get("password")

        # Verificar si el correo electrónico existe en la base de datos
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Credenciales incorrectas."}, status=400)

        # Verificar la contraseña
        if check_password(password, user.password):
            return Response({"message": "Inicio de sesión exitoso."}, status=200)
        else:
            return Response({"error": "Credenciales incorrectas."}, status=400)
        
# Representante: Recuperar un registro único
class RepresentanteRetrieveView(RetrieveAPIView):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer

# Alumno: Recuperar un registro único
class AlumnoRetrieveView(RetrieveAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

# Curso: Recuperar un registro único
class CursoRetrieveView(RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Matricula: Recuperar un registro único
class MatriculaRetrieveView(RetrieveAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

# Curriculo: Recuperar un registro único
class CurriculoRetrieveView(RetrieveAPIView):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer

# Aula: Recuperar un registro único
class AulaRetrieveView(RetrieveAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

# Evaluacion: Recuperar un registro único
class EvaluacionRetrieveView(RetrieveAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer

# Asistencia: Recuperar un registro único
class AsistenciaRetrieveView(RetrieveAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

# Curso_Matricula: Recuperar un registro único
class Curso_MatriculaRetrieveView(RetrieveAPIView):
    queryset = Curso_Matricula.objects.all()
    serializer_class = Curso_MatriculaSerializer

# Horario: Recuperar un registro único
class HorarioRetrieveView(RetrieveAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

# Horario_Curso: Recuperar un registro único
class Horario_CursoRetrieveView(RetrieveAPIView):
    queryset = Horario_Curso.objects.all()
    serializer_class = Horario_CursoSerializer


       
# Representante
class RepresentanteRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer

# Alumno
class AlumnoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

# Curso
class CursoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Matricula
class MatriculaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

# Curriculo
class CurriculoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer

# Aula
class AulaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

# Evaluacion
class EvaluacionRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer

# Asistencia
class AsistenciaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

# Curso_Matricula
class Curso_MatriculaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Curso_Matricula.objects.all()
    serializer_class = Curso_MatriculaSerializer

# Horario
class HorarioRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

# Horario_Curso
class Horario_CursoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Horario_Curso.objects.all()
    serializer_class = Horario_CursoSerializer
    
    
