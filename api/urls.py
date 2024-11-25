from django.urls import path
from .views import AlumnoRetrieveView, AsistenciaListCreateView, AsistenciaRetrieveView, AulaListCreateView, AulaRetrieveView, CurriculoListCreateView, CurriculoRetrieveView, Curso_MatriculaListCreateView, Curso_MatriculaRetrieveView, CursoRetrieveView, EvaluacionListCreateView, EvaluacionRetrieveView, Horario_CursoListCreateView, Horario_CursoRetrieveView, HorarioListCreateView, HorarioRetrieveView, LoginView, MatriculaRetrieveView, RepresentanteListCreateView, AlumnoListCreateView, CursoListCreateView, MatriculaListCreateView, RepresentanteRetrieveView, UserListCreateView

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
    path('representante/<int:pk>/', RepresentanteRetrieveView.as_view(), name='representante-detail'),
    path('alumno/<int:pk>/', AlumnoRetrieveView.as_view(), name='alumno-detail'),
    path('curso/<int:pk>/', CursoRetrieveView.as_view(), name='curso-detail'),
    path('matricula/<int:pk>/', MatriculaRetrieveView.as_view(), name='matricula-detail'),
    path('curriculo/<int:pk>/', CurriculoRetrieveView.as_view(), name='curriculo-detail'),
    path('aula/<int:pk>/', AulaRetrieveView.as_view(), name='aula-detail'),
    path('evaluacion/<int:pk>/', EvaluacionRetrieveView.as_view(), name='evaluacion-detail'),
    path('asistencia/<int:pk>/', AsistenciaRetrieveView.as_view(), name='asistencia-detail'),
    path('curso_matricula/<int:pk>/', Curso_MatriculaRetrieveView.as_view(), name='curso_matricula-detail'),
    path('horario/<int:pk>/', HorarioRetrieveView.as_view(), name='horario-detail'),
    path('horario_curso/<int:pk>/', Horario_CursoRetrieveView.as_view(), name='horario_curso-detail'),   
]

