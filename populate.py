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


def poblar_representantes(n):
    """Crea 'n' representantes ficticios."""
    for _ in range(n):
        representante = Parent(
            dni=fake.unique.random_int(min=10000000, max=99999999),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number()[0:9],
            address=fake.address()
        )
        representante.save()
        print(f"Representante creado: {representante}")


def poblar_alumnos(n):
    """Crea 'n' alumnos ficticios."""
    representantes = list(Parent.objects.all())
    if not representantes:
        print(
            "No hay representantes disponibles. Por favor, primero genera representantes.")
        return

    for _ in range(n):
        representante = random.choice(representantes)
        fecha_nacimiento = generar_fecha_nacimiento_aleatoria()
        fecha_inscripcion = generar_fecha_inscripcion(fecha_nacimiento)

        alumno = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dni=fake.unique.random_int(min=10000000, max=99999999),
            birth_date=fecha_nacimiento,
            enrollment_date=fecha_inscripcion,
            address=fake.address(),
            parent=representante
        )
        alumno.save()
        print(f"Alumno creado: {alumno}")


def poblar_curriculos(n):
    """Crea 'n' currículos ficticios."""
    for _ in range(n):
        curriculo = Curriculum(
            name=fake.word(),
            year=random.randint(2018, 2024),
            status=random.choice(['active', 'inactive', 'deleted']),
            school_year=random.randint(2015, date.today().year)
        )
        curriculo.save()
        print(f"Currículo creado: {curriculo}")


def poblar_cursos(n):
    """Crea 'n' cursos ficticios."""
    curriculos = list(Curriculum.objects.all())
    if not curriculos:
        print("No hay currículos disponibles. Por favor, primero genera currículos.")
        return

    for _ in range(n):
        curso = Course(
            name=fake.word(),
            weekly_hours=random.randint(2, 5),
            curriculum=random.choice(curriculos)
        )
        curso.save()
        print(f"Curso creado: {curso}")


def poblar_aulas(n):
    """Crea 'n' aulas ficticias."""
    for _ in range(n):
        aula = Classroom(
            name=fake.word(),
            capacity=random.randint(10, 50)
        )
        aula.save()
        print(f"Aula creada: {aula}")


def poblar_matriculas(n):
    """Crea 'n' matrículas ficticias."""
    alumnos = list(Student.objects.all())
    curriculos = list(Curriculum.objects.all())
    

    if not alumnos or not curriculos:
        print("No hay alumnos o currículos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        matricula = Enrollment(
            student=random.choice(alumnos),
            curriculum=random.choice(curriculos),
            enrollment_date=generar_fecha_aleatoria(2023, date.today().year),
            status=random.choice(['active', 'inactive', 'suspended']),
        )
        matricula.save()
        courses = list(Course.objects.all())
        addCourses = random.choice(courses)
        matricula.courses.add(addCourses)
        print(f"Matrícula creada: {matricula}")


def poblar_evaluaciones(n):
    """Crea 'n' evaluaciones ficticias."""
    alumnos = list(Student.objects.all())
    cursos = list(Course.objects.all())

    if not alumnos or not cursos:
        print("No hay alumnos o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        evaluacion = Evaluation(
            student=random.choice(alumnos),
            course=random.choice(cursos),
            type=random.choice(['parcial', 'final', 'práctica']),
            grade=random.randint(0, 20),
            date=generar_fecha_aleatoria(2020, date.today().year)
        )
        evaluacion.save()
        print(f"Evaluación creada: {evaluacion}")


def poblar_asistencias(n):
    """Crea 'n' asistencias ficticias."""
    alumnos = list(Student.objects.all())
    cursos = list(Course.objects.all())

    if not alumnos or not cursos:
        print("No hay alumnos o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        asistencia = Attendance(
            student=random.choice(alumnos),
            date=generar_fecha_aleatoria(2020, date.today().year),
            status=random.choice(['presente', 'ausente', 'justificado']),
            course=random.choice(cursos)
        )
        asistencia.save()
        print(f"Asistencia creada: {asistencia}")


def poblar_horarios(n):
    """Crea 'n' horarios ficticios."""
    aulas = list(Classroom.objects.all())
    if not aulas:
        print("No hay aulas disponibles. Por favor, genera datos para ellas primero.")
        return

    for _ in range(n):
        hora_inicio = fake.date_time_between(start_date="-1y", end_date="now")
        hora_fin = hora_inicio + timedelta(hours=random.randint(1, 3))
        horario = Schedule(
            day=random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
            start_time=hora_inicio,
            end_time=hora_fin,
            classroom=random.choice(aulas)
        )
        horario.save()
        print(f"Horario creado: {horario}")


def poblar_horarios_cursos(n):
    """Crea 'n' relaciones de horario-curso ficticias."""
    horarios = list(Schedule.objects.all())
    cursos = list(Course.objects.all())

    if not horarios or not cursos:
        print("No hay horarios o cursos disponibles. Por favor, genera datos para ellos primero.")
        return

    for _ in range(n):
        horario_curso = CourseSchedule(
            course=random.choice(cursos),
            schedule=random.choice(horarios)
        )
        horario_curso.save()
        print(f"Horario-Curso creado: {horario_curso}")

from django.contrib.auth.models import Group
def poblar_grupos():
    """Crea los grupos de usuarios."""
    for grupo in ["Management", "Teacher"]:
        nuevo_grupo, _ = Group.objects.get_or_create(name=grupo)
        print(f"Grupo creado: {nuevo_grupo}")


def poblar_usuarios(n):
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
            name=random.choice(["Management"]))
        usuario.groups.add(groups)
        print(f"Usuario creado: {usuario}")


def poblar_docentes(n):

    for _ in range(n):
        usuario = User(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
        )
        usuario.save()
        usuario.groups.add(Group.objects.get(id=2))
        docente = Teacher(
            user=usuario,
            specialty=fake.word()
        )
        docente.save()
        print(f"Docente creado: {docente}")


def poblar_materias(n):
    for _ in range(n):
        materia = Subject(
            name=fake.word(),
            course=random.choice(Course.objects.all()),
            teacher=random.choice(Teacher.objects.all())
        )
        materia.save()
        print(f"Materia creada: {materia}")

# Ejecutar todas las funciones


def poblar_todos():
    poblar_representantes(50)
    poblar_alumnos(50)
    poblar_curriculos(3)
    poblar_cursos(20)
    poblar_aulas(30)
    poblar_matriculas(150)
    poblar_evaluaciones(10)
    poblar_asistencias(100)
    poblar_horarios(10)
    poblar_horarios_cursos(10)
    poblar_grupos()
    # poblar_usuarios(10)
    poblar_docentes(3)
    poblar_materias(5)


#poblar_todos()
