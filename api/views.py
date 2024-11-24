from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics
from .models import Asistencia, Aula, Curso_Matricula, Evaluacion, Horario, Horario_Curso, Representante, Alumno, Curso, Matricula, Curriculo
from .serializers import AsistenciaSerializer, AulaSerializer, CurriculoSerializer, Curso_MatriculaSerializer, EvaluacionSerializer, Horario_CursoSerializer, HorarioSerializer, RepresentanteSerializer, AlumnoSerializer, CursoSerializer, MatriculaSerializer, UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

class RepresentanteListCreateView(generics.ListCreateAPIView):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer

class AlumnoListCreateView(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CursoListCreateView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MatriculaListCreateView(generics.ListCreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    
class CurriculoListCreateView(generics.ListCreateAPIView):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer
    
class AulaListCreateView(generics.ListCreateAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    
class EvaluacionListCreateView(generics.ListCreateAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer

class AsistenciaListCreateView(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class Curso_MatriculaListCreateView(generics.ListCreateAPIView):
    queryset = Curso_Matricula.objects.all()
    serializer_class = Curso_MatriculaSerializer

class HorarioListCreateView(generics.ListCreateAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class Horario_CursoListCreateView(generics.ListCreateAPIView):
    queryset = Horario_Curso.objects.all()
    serializer_class = Horario_CursoSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
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