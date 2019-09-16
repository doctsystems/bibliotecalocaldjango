from django.db import models

# Utilizado para generar URL invirtiendo los patrones de URL
from django.urls import reverse

# Create your models here.

class MyModelName(models.Model):
	"""	Una clase típica definiendo un modelo, derivado desde la clase Model. """

	# Campos
	my_field_name = models.CharField(max_length=20, help_text="Enter field documentation.")

	# Metadata
	class Meta: 
		ordering = ["-my_field_name"]

	# Métodos
	def get_absolute_url(self):
		""" Devuelve la url para acceder a una instancia particular de MyModelName. """
		return reverse('model-detail-view', args=[str(self.id)])

	def __str__(self):
		""" Cadena para representar el objeto MyModelName (en el sitio de Admin, etc.) """
		return self.field_name

class Autor(models.Model):
	""" Modelo que representa un autor """
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	fecha_fallecimiento = models.DateField('Fallecimiento', null=True, blank=True)

	def get_absolute_url(self):
		""" Retorna la url para acceder a una instancia particular de un autor. """
		return reverse('autor-detalle', args=[str(self.id)])

	def __str__(self):
		""" String para representar el Objeto Modelo """
		return '%s, %s' % (self.apellido, self.nombre)

class Genero(models.Model):
	""" Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.). """
	name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.).")

	def __str__(self):
		"""	Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración) """
		return self.name

class Idioma(models.Model):
	"""Modelo que representa un idioma (por ejemplo, inglés, francés, japonés, etc.)"""
	idioma = models.CharField(max_length=200, help_text="Ingrese el idioma natural del libro (por ejemplo, inglés, francés, japonés, etc.).")

	def __str__(self):
		"""String for representing the Model object (in Admin site etc.)"""
		return self.idioma

class Libro(models.Model):
	""" Modelo que representa un libro (pero no un Ejemplar específico)."""
	titulo = models.CharField(max_length=200)

	# ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
	autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
	resumen = models.TextField(max_length=1000, help_text="Ingrese un breve resumen del libro.")
	isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN number</a>')
	# ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
	genero = models.ManyToManyField('Genero', help_text="Seleccione un genero para este libro.")
	idioma = models.ForeignKey('Idioma', on_delete=models.SET_NULL, null=True)

	def display_generos(self):
		""" Crea una cadena con los Géneros al que pertenece un Libro. Esto es necesario para mostrar en Admin. """
		return ', '.join([ genero.name for genero in self.genero.all()[:3] ])
	
	""" Crea una discripcion corta para los Géneros para mostrar como cabecera de tabla en Admin. """
	display_generos.short_description = 'Géneros'

	def __str__(self):
		""" String que representa al objeto Libro """
		return self.titulo

	def get_absolute_url(self):
		""" Devuelve el URL a una instancia particular de Libro """
		return reverse('libro-detalle', args=[str(self.id)])

# Requerida para las instancias de libros únicos
import uuid
from datetime import date
# Requerido para asignar al usuario como prestatario.
from django.contrib.auth.models import User

class LibroCopia(models.Model):
	"""	Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca). """
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca.")
	libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True) 
	imprenta = models.CharField(max_length=200)
	fecha_devolucion = models.DateField(null=True, blank=True)
	prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	@property
	def is_atrasado(self):
		if self.fecha_devolucion and date.today() > self.fecha_devolucion:
			return True
		return False

	LOAN_STATUS = (
	    ('m', 'Maintenance'),	# mantenimiento
	    ('o', 'On loan'),		# en prestamo
	    ('a', 'Available'),		# disponible
	    ('r', 'Reserved'),		# reservado
	)

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro.')

	class Meta:
		ordering = ["fecha_devolucion"]
		permissions = (("puede_marcar_devuelto", "Establecer libro como devuelto"),)

	def __str__(self):
		""" String para representar el Objeto del Modelo """
		return '%s (%s)' % (self.id, self.libro.titulo)
		# return '{0} ({1})'.format(self.id,self.libro.titulo) 
		# return f'{self.id} ({self.libro.titulo})'

