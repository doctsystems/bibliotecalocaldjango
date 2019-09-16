from django.contrib import admin

from .models import Autor, Genero, Libro, LibroCopia, Idioma

# Register your models here.

# admin.site.register(Libro)
# admin.site.register(Autor)
admin.site.register(Genero)
# admin.site.register(LibroCopia)
admin.site.register(Idioma)

# Clase para edición en cadena de registros asociados.
class LibroInline(admin.StackedInline): # TabularInline (Horizontal) y StackedInline (Vertical)
	model = Libro

# Define la clase admin
class AutorAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'apellido', 'fecha_nacimiento', 'fecha_fallecimiento')

	# El atributo fields lista solo los campos que se van a desplegar en el formulario, en orden. 
	fields = ['nombre', 'apellido', ('fecha_nacimiento', 'fecha_fallecimiento')]

	# Añadir la información de Libro dentro del detalle de Autor.
	inlines = [LibroInline]

# Registre la clase admin con el modelo asociado.
admin.site.register(Autor, AutorAdmin)

# Clase para edición en cadena de registros asociados.
class LibroCopiaInline(admin.TabularInline): # TabularInline (Horizontal) y StackedInline (Vertical)
	model = LibroCopia

# Registre las clases de Admin para el Libro usando el decorador
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'autor', 'display_generos')

	# Añadir la información de LibroCopia dentro del detalle de Libro.
	inlines = [LibroCopiaInline]

# Registre las clases de Admin para LibroCopia usando el decorador
@admin.register(LibroCopia) 
class LibroCopiaAdmin(admin.ModelAdmin):
	list_display = ('libro', 'status', 'prestatario', 'fecha_devolucion', 'id')
	list_filter = ('status', 'fecha_devolucion')

	# Añadir "secciones" para agrupar información relacionada del modelo dentro del formulario de detalle, usando el atributo fieldsets.
	fieldsets = (
		(None, {
			'fields': ('libro', 'imprenta', 'id')
		}),
		('Disponibilidad', {
			'fields': ('status', 'fecha_devolucion', 'prestatario')
		}),
	)

