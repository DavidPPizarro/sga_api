from faker import Faker
from datetime import date, timedelta, datetime
import random
import django
import os
# Configura la variable de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_academica.settings')

# Inicializa Django
django.setup()

# Importar modelos
from api.models import *

# Inicializar Faker
fake = Faker()

# Funciones para generar fechas en rangos


def generar_fecha_nacimiento_aleatoria(edad_minima=7, edad_maxima=13):
    """Genera una fecha de nacimiento aleatoria para alumnos entre 7 y 13 años."""
    hoy = date.today()
    anio_inicio = hoy.year - edad_maxima
    anio_fin = hoy.year - edad_minima
    anio = random.randint(anio_inicio, anio_fin)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)  # Evitar problemas con días inválidos
    return date(anio, mes, dia)


def generar_fecha_inscripcion(fecha_nacimiento):
    """Genera una fecha de inscripción lógica posterior a la fecha de nacimiento."""
    edad_inscripcion = random.randint(6, 7)
    fecha_inscripcion = fecha_nacimiento + \
        timedelta(days=edad_inscripcion * 365)
    if fecha_inscripcion > date.today():
        fecha_inscripcion = date.today()
    return fecha_inscripcion


def generar_fecha_aleatoria(anio_inicio, anio_fin):
    """Genera una fecha aleatoria entre dos años dados."""
    anio = random.randint(anio_inicio, anio_fin)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)  # Evitar días inválidos
    return date(anio, mes, dia)

# Funciones para poblar modelos


def poblar_representantes(n=50):
    """Crea 'n' representantes ficticios."""
    for _ in range(n):
        representante = Representante(
            dni=fake.unique.random_int(min=10000000, max=99999999),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            # Asegúrate de que no exceda 15 caracteres
            telefono=fake.phone_number()[:15],
            direccion=fake.address()
        )
        representante.save()
        print(f"Representante creado: {representante}")


def poblar_alumnos(n=50):
    """Crea 'n' alumnos ficticios."""
    representantes = list(Representante.objects.all())
    if not representantes:
        print(
            "No hay representantes disponibles. Por favor, primero genera representantes.")
        return

    for _ in range(n):
        representante = random.choice(representantes)
        fecha_nacimiento = generar_fecha_nacimiento_aleatoria()
        fecha_inscripcion = generar_fecha_inscripcion(fecha_nacimiento)

        alumno = Alumno(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            dni=fake.unique.random_int(min=10000000, max=99999999),
            fecha_nacimiento=fecha_nacimiento,
            fecha_inscripcion=fecha_inscripcion,
            direccion=fake.address(),
            id_representante=representante
        )
        alumno.save()
        print(f"Alumno creado: {alumno}")


def poblar_curriculos(n=3):
    """Crea 'n' currículos ficticios."""
    for _ in range(n):
        curriculo = Curriculo(
            nombre=fake.word(),
            anio=random.randint(2010, 2023),
            estado=random.choice(['activo', 'inactivo', 'eliminado'])
        )
        curriculo.save()
        print(f"Currículo creado: {curriculo}")


def poblar_cursos(n=40):
    """Crea 'n' cursos ficticios."""
    curriculos = list(Curriculo.objects.all())
    if not curriculos:
        print("No hay currículos disponibles. Por favor, primero genera currículos.")
        return

    for _ in range(n):
        curso = Curso(
            nombre=fake.word(),
            horas_semanales=random.randint(1, 10),
            id_curriculo=random.choice(curriculos)
        )
        curso.save()
        print(f"Curso creado: {curso}")


def poblar_aulas(n=30):
    """Crea 'n' aulas ficticias."""
    for _ in range(n):
        aula = Aula(
            nombre=f"Aula {fake.word()}",
            capacidad=random.randint(20, 50)
        )
        aula.save()
        print(f"Aula creada: {aula}")


def poblar_matriculas(n=50):
    """Crea 'n' matrículas ficticias."""
    alumnos = list(Alumno.objects.all())
    curriculos = list(Curriculo.objects.all())

    if not alumnos or not curriculos:
        print("No hay alumnos o currículos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        matricula = Matricula(
            id_alumno=random.choice(alumnos),
            id_curriculo=random.choice(curriculos),
            fecha_matricula=generar_fecha_aleatoria(2015, date.today().year),
            estado=random.choice(['activo', 'inactivo', 'suspendido'])
        )
        matricula.save()
        print(f"Matrícula creada: {matricula}")


def poblar_evaluaciones(n=10):
    """Crea 'n' evaluaciones ficticias."""
    alumnos = list(Alumno.objects.all())
    cursos = list(Curso.objects.all())

    if not alumnos or not cursos:
        print("No hay alumnos o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        evaluacion = Evaluacion(
            id_alumno=random.choice(alumnos),
            id_curso=random.choice(cursos),
            tipo=random.choice(['continua', 'parcial']),
            nota=round(random.uniform(0, 20), 2),
            fecha=generar_fecha_aleatoria(2020, date.today().year)
        )
        evaluacion.save()
        print(f"Evaluación creada: {evaluacion}")


def poblar_asistencias(n=100):
    """Crea 'n' asistencias ficticias."""
    alumnos = list(Alumno.objects.all())
    cursos = list(Curso.objects.all())

    if not alumnos or not cursos:
        print("No hay alumnos o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        asistencia = Asistencia(
            id_alumno=random.choice(alumnos),
            id_curso=random.choice(cursos),
            fecha=generar_fecha_aleatoria(2020, date.today().year),
            estado=random.choice(['asistio', 'no asistio'])
        )
        asistencia.save()
        print(f"Asistencia creada: {asistencia}")


def poblar_horarios(n=10):
    """Crea 'n' horarios ficticios."""
    aulas = list(Aula.objects.all())
    if not aulas:
        print("No hay aulas disponibles. Por favor, genera datos para ellas primero.")
        return

    for _ in range(n):
        hora_inicio = fake.date_time_between(start_date="-1y", end_date="now")
        hora_fin = hora_inicio + timedelta(hours=random.randint(1, 3))
        horario = Horario(
            dia=random.choice(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'])[
                :15],  # Truncar a 15 caracteres
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            id_aula=random.choice(aulas)
        )
        horario.save()
        print(f"Horario creado: {horario}")


def poblar_horarios_cursos(n=10):
    """Crea 'n' relaciones de horario-curso ficticias."""
    horarios = list(Horario.objects.all())
    cursos = list(Curso.objects.all())

    if not horarios or not cursos:
        print("No hay horarios o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        horario_curso = Horario_Curso(
            id_curso=random.choice(cursos),
            id_horario=random.choice(horarios)
        )
        horario_curso.save()
        print(f"Horario-Curso creado: {horario_curso}")

from django.contrib.auth.models import Group
def poblar_grupos():
    """Crea los grupos de usuarios."""
    for grupo in ["Administración", "Dirección", "Docente"]:
        nuevo_grupo, _ = Group.objects.get_or_create(name=grupo)
        print(f"Grupo creado: {nuevo_grupo}")


def poblar_usuarios(n=10):
    """Crea 'n' usuarios ficticios."""
    for _ in range(n):
        usuario = User(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
        )
        usuario.save()

        groups = Group.objects.get(
            name=random.choice(["Administración", "Dirección"]))
        usuario.groups.add(groups)
        print(f"Usuario creado: {usuario}")


def poblar_docentes(n=10):

    for _ in range(n):
        usuario = User(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
        )
        usuario.save()
        usuario.groups.add(Group.objects.get(id=3))
        docente = Teacher(
            user=usuario,
            specialty=fake.word()
        )
        docente.save()
        print(f"Docente creado: {docente}")

def poblar_materias(n=10):
    for _ in range(n):
        materia = Materia(
            name=fake.word(),
            id_course=random.choice(Curso.objects.all()),
            id_teacher=random.choice(Teacher.objects.all())
        )
        materia.save()
        print(f"Materia creada: {materia}")

# Ejecutar todas las funciones


def poblar_todos():
    poblar_representantes(50)
    poblar_alumnos(50)
    poblar_curriculos(3)
    poblar_cursos(40)
    poblar_aulas(30)
    poblar_matriculas(50)
    poblar_evaluaciones(10)
    poblar_asistencias(100)
    poblar_horarios(10)
    poblar_horarios_cursos(10)
    poblar_grupos()
    poblar_usuarios(10)
    poblar_docentes(10)
    poblar_materias(10)

# Llamar a poblar_todos para poblar la base de datos
poblar_todos()
