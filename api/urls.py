from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'materias', MateriaViewSet, 'materias')
router.register(r'teachers', TeacherViewSet, 'teachers')
router.register(r'representantes', RepresentanteViewSet, 'representantes')
router.register(r'alumnos', AlumnoViewSet, 'alumnos')
router.register(r'evaluaciones', EvaluacionViewSet, 'evaluaciones')
urlpatterns = [
    path('', include(router.urls)),
    path('cursos/', CursoListCreateView.as_view(), name='curso-list'),
    path('matriculas/', MatriculaListCreateView.as_view(), name='matricula-list'),
    path('curriculo/', CurriculoListCreateView.as_view(), name='curriculo-list'),
    path('aula/', AulaListCreateView.as_view(), name='aula-list'),
    path('asistencia/', AsistenciaListCreateView.as_view(), name='asistencia-list'),
    path('curso_matricula/', Curso_MatriculaListCreateView.as_view(), name='cursomatricula-list'),
    path('horario/', HorarioListCreateView.as_view(), name='horario-list'),
    path('horario_curso/', Horario_CursoListCreateView.as_view(), name='horariocurso-list'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('cursos/<int:pk>/', CursoRetrieveView.as_view(), name='curso-detail'),
    path('matriculas/<int:pk>/', MatriculaRetrieveView.as_view(), name='matricula-detail'),
    path('curriculo/<int:pk>/', CurriculoRetrieveView.as_view(), name='curriculo-detail'),
    path('aula/<int:pk>/', AulaRetrieveView.as_view(), name='aula-detail'),
    path('asistencia/<int:pk>/', AsistenciaRetrieveView.as_view(), name='asistencia-detail'),
    path('curso_matricula/<int:pk>/', Curso_MatriculaRetrieveView.as_view(), name='curso_matricula-detail'),
    path('horario/<int:pk>/', HorarioRetrieveView.as_view(), name='horario-detail'),
    path('horario_curso/<int:pk>/', Horario_CursoRetrieveView.as_view(), name='horario_curso-detail'),   
    # Rutas para eliminación (DELETE)
    path('cursos/<int:pk>/delete/', CursoRetrieveDestroyView.as_view(), name='curso-delete'),
    path('matriculas/<int:pk>/delete/', MatriculaRetrieveDestroyView.as_view(), name='matricula-delete'),
    path('curriculo/<int:pk>/delete/', CurriculoRetrieveDestroyView.as_view(), name='curriculo-delete'),
    path('aula/<int:pk>/delete/', AulaRetrieveDestroyView.as_view(), name='aula-delete'),
    path('asistencias/<int:pk>/delete/', AsistenciaRetrieveDestroyView.as_view(), name='asistencia-delete'),
    path('curso_matricula/<int:pk>/delete/', Curso_MatriculaRetrieveDestroyView.as_view(), name='curso-matricula-delete'),
    path('horarios/<int:pk>/delete/', HorarioRetrieveDestroyView.as_view(), name='horario-delete'),
    path('horario_curso/<int:pk>/delete/', Horario_CursoRetrieveDestroyView.as_view(), name='horario-curso-delete'),
    #Actualizar
    path('cursos/<int:pk>/update/', CursoUpdateView.as_view(), name='curso-update'),
    path('matriculas/<int:pk>/update/', MatriculaUpdateView.as_view(), name='matricula-update'),
    path('curriculo/<int:pk>/update/', CurriculoUpdateView.as_view(), name='curriculo-update'),
    path('aula/<int:pk>/update/', AulaUpdateView.as_view(), name='aula-update'),    
    path('asistencia/<int:pk>/update/', AsistenciaUpdateView.as_view(), name='asistencia-update'),
    path('curso_matricula/<int:pk>/update/', Curso_MatriculaUpdateView.as_view(), name='curso-matricula-update'),
    path('horario/<int:pk>/update/', HorarioUpdateView.as_view(), name='horario-update'),
    path('horario_curso/<int:pk>/update/', Horario_CursoUpdateView.as_view(), name='horario-curso-update'),
]

