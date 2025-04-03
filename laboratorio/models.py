from django.db import models


# Create your models here.
class Menu(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class MenuOpciones(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    programa = models.CharField(max_length=200)

    def __str__(self):
        return self.menu.nombre + " - " + self.nombre


class Consultorios(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_id = models.CharField(max_length=2, default="1")  # FK a Turnos (laboratorio, consulta, lentes, etc)
    disponible = models.CharField(max_length=2, default="N")

    def __str__(self):
        return str(self.id) + " - " + self.nombre


class Medicos(models.Model):
    consultorio = models.ForeignKey(Consultorios, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.nombre + " - " + self.consultorio.nombre


class Productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class CodigoPostal(models.Model):
    ciudad = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=6)
    estado = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    colonia = models.CharField(max_length=200)


class Clientes(models.Model):
    nombre = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=200)
    apellido_materno = models.CharField(max_length=200)
    telefono1 = models.CharField(max_length=200)
    telefono2 = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    codigopostal = models.CharField(max_length=20)
    calle = models.CharField(max_length=200, default="")
    numero_int = models.CharField(max_length=20, default="")
    numero_ext = models.CharField(max_length=20, default="")
    colonia = models.CharField(max_length=20, default="")
    fecha_nac = models.CharField(max_length=20, default="")
    rfc = models.CharField(max_length=13, default="")

    def __str__(self):
        return str(self.id) + " - " + self.nombre


class Citas(models.Model):
    consultorio_id = models.CharField(max_length=10)
    medico_id = models.CharField(max_length=10)
    cliente_id = models.CharField(max_length=10)
    servicio_id = models.CharField(max_length=10, default="0")
    precio = models.CharField(max_length=10, default="0")
    fecha = models.CharField(max_length=15)
    hora = models.CharField(max_length=10)
    observaciones = models.TextField(max_length=200)
    checkin_fecha = models.TextField(max_length=20, default='')
    checkin_edad = models.TextField(max_length=6, default='')
    checkin_sexo = models.TextField(max_length=12, default='')
    checkin_peso = models.TextField(max_length=12, default='')
    checkin_talla = models.TextField(max_length=12, default='')
    checkin_presion_arterial = models.TextField(max_length=12, default='')
    checkin_frecuencia_cardiaca = models.TextField(max_length=12, default='')
    checkin_frecuencia_respiratoria = models.TextField(max_length=12, default='')
    checkin_temperatura = models.TextField(max_length=12, default='')
    checkin_resumen = models.TextField(max_length=500, default='')
    checkin_exploracion_fisica = models.TextField(max_length=500, default='')
    checkin_resultado_servicios_auxiliares = models.TextField(max_length=500, default='')
    checkin_problemas_clinicos = models.TextField(max_length=500, default='')
    checkin_indicaciones_medicas = models.TextField(max_length=500, default='')
    checkin_pronostico = models.TextField(max_length=500, default='')
    checkout_hora = models.TextField(max_length=12, default='')
    turno_num = models.IntegerField(default=0)

    def __str__(self):
        return self.fecha + " - " + self.hora


class Turnos(models.Model):
    descripcion = models.CharField(max_length=100)
    tipo_id = models.CharField(max_length=2, default="1")  # (laboratorio, consulta, lentes, etc)

    def __str__(self):
        return str(self.id) + " - " + self.descripcion + " - " + self.tipo_id


class Turnos_agenda(models.Model):
    turno_id = models.CharField(max_length=10)
    turno_num = models.IntegerField(default=1)
    fecha = models.CharField(max_length=100)
    hora = models.CharField(max_length=10)
    hora_atencion = models.CharField(max_length=10)
    mostrado = models.CharField(max_length=1, default='S')
    liberado = models.CharField(max_length=1, default='N')
    producto_id = models.CharField(max_length=10, default='6')
    consultorio = models.CharField(max_length=100, default='')
    medico_id = models.CharField(max_length=2, default='0')
    cliente_id = models.CharField(max_length=2, default='0')


    def __str__(self):
        return str(self.id) + " - " + self.turno_id + " - " + self.fecha + " - " + self.hora


class Consultorios_Turnos(models.Model):
    cons_id = models.CharField(max_length=2)
    turno_num = models.CharField(max_length=2)
    nombre = models.CharField(max_length=20)
