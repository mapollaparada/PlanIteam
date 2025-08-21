
from django.db import models
from django.contrib.auth.models import User

class Espacio(models.Model):
	nombre = models.CharField(max_length=100)
	usuarios = models.ManyToManyField(User, related_name='espacios', blank=True)
    
	def __str__(self):
		return self.nombre

class Categoria(models.Model):
	nombre = models.CharField(max_length=100)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='categorias')  # Para categorías personales
	espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, null=True, blank=True, related_name='categorias')  # Para categorías compartidas

	def __str__(self):
		return self.nombre

class Nota(models.Model):
	titulo = models.CharField(max_length=200)
	contenido = models.TextField(blank=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas')
	espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL, null=True, blank=True, related_name='notas')
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='notas')
    
	def __str__(self):
		return self.titulo

class Tarea(models.Model):
	titulo = models.CharField(max_length=200)
	descripcion = models.TextField(blank=True)
	fecha_inicio = models.DateField(null=True, blank=True)
	fecha_fin = models.DateField(null=True, blank=True)
	estado = models.CharField(max_length=20, default='pendiente')
	recurrencia = models.CharField(
		max_length=20,
		choices=[
			('ninguna', 'Ninguna'),
			('diaria', 'Diaria'),
			('semanal', 'Semanal'),
			('mensual', 'Mensual'),
		],
		default='ninguna',
		blank=True
	)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
	espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')

	def __str__(self):
		return self.titulo

class Presupuesto(models.Model):
	titulo = models.CharField(max_length=200)
	descripcion = models.TextField(blank=True)
	link = models.TextField(blank=True)
	precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presupuestos')
	espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL, null=True, blank=True, related_name='presupuestos')
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='presupuestos')
    
	def __str__(self):
		return self.titulo
