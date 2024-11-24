from django.db import models

# Representante del alumno
class Representante(models.Model):
    id_representante = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Alumno
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, default='')
    fecha_nacimiento = models.DateField(auto_now_add=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=100, default='Desconocido')
    id_representante = models.ForeignKey(Representante, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#Curriculo
class Curriculo(models.Model):
    id_curriculo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField()
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('eliminado', 'Eliminado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='inactivo')
    anio_escolar = models.IntegerField
    
    def __str__(self):
        return  f"{self.nombre} {self.anio}"
    
# Curso
class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    horas_semanales = models.IntegerField()
    id_curriculo = models.ForeignKey(Curriculo, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nombre

# Aula
class Aula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

# Matricula
class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE)
    fecha_matricula = models.DateField(auto_now=True)
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')  
    
    def __str__(self):
        return f"Matricula de {self.id_alumno} en {self.id_curso}"

# Evaluacion
class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    TIPO_CHOICES = [
        ('continua', 'Continua'),
        ('parcial', 'Parcial'),        
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nota = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Evaluación de {self.id_alumno} en {self.id_curso}"
    
# Asistencia
class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('asistio','Asistio'),
        ('no asistio','No Asistio'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='no asistio')
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Asistencia de {self.id_alumno} - {self.fecha}"

 # Curso Matricula
class Curso_Matricula(models.Model):
    id_curso_matricula = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_curso_matricula
    
# Horario
class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=15)
    hora_inicio =  models.DateTimeField()
    hora_fin =  models.DateTimeField()
    id_aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_horario
    
# Horario Curso
class Horario_Curso(models.Model):
    id_horario_curso = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    id_horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_horario_curso

