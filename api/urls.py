from django.urls import path
from .views import AsistenciaListCreateView, AulaListCreateView, CurriculoListCreateView, Curso_MatriculaListCreateView, EvaluacionListCreateView, Horario_CursoListCreateView, HorarioListCreateView, LoginView, RepresentanteListCreateView, AlumnoListCreateView, CursoListCreateView, MatriculaListCreateView, UserListCreateView

urlpatterns = [
    path('representantes/', RepresentanteListCreateView.as_view(), name='representante-list'),
    path('alumnos/', AlumnoListCreateView.as_view(), name='alumno-list'),
    path('cursos/', CursoListCreateView.as_view(), name='curso-list'),
    path('matriculas/', MatriculaListCreateView.as_view(), name='matricula-list'),
    path('curriculo/', CurriculoListCreateView.as_view(), name='curriculo-list'),
    path('aula/', AulaListCreateView.as_view(), name='aula-list'),
    path('evaluacion/', EvaluacionListCreateView.as_view(), name='evaluacion-list'),
    path('asistencia/', AsistenciaListCreateView.as_view(), name='asistencia-list'),
    path('cursomatricula/', Curso_MatriculaListCreateView.as_view(), name='cursomatricula-list'),
    path('horario/', HorarioListCreateView.as_view(), name='horario-list'),
    path('horariocurso/', Horario_CursoListCreateView.as_view(), name='horariocurso-list'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    
]

