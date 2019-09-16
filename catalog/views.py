from django.shortcuts import render

from .models import Libro, Autor, LibroCopia, Genero

# Create your views here.

def home(request):
	"""	Función vista para la página inicio del sitio. """

	# Genera contadores de algunos de los objetos principales
	num_libros = Libro.objects.all().count()
	num_copias = LibroCopia.objects.all().count()

	# Libros disponibles (status = 'a')
	num_copias_disponibles = LibroCopia.objects.filter(status__exact='a').count()

	num_autores = Autor.objects.count()  # El 'all()' esta implícito por defecto.

	num_generos = Genero.objects.count()

	# Número de visitas a esta vista, contadas en la variable de sesión.
	num_visitas = request.session.get('num_visitas', 0)
	request.session['num_visitas'] = num_visitas + 1

	# Renderiza la plantilla HTML home.html con los datos en la variable contexto
	return render(
		request,
		'home.html',
		context={'num_libros':num_libros,'num_generos':num_generos,'num_copias':num_copias,'num_copias_disponibles':num_copias_disponibles,'num_autores':num_autores,'num_visitas':num_visitas}, # num_visitas anexado
	)

# Listas genéricas y vistas de detalle
from django.views import generic

class LibroListView(generic.ListView):
	model = Libro
	paginate_by = 3

class LibroDetailView(generic.DetailView):
    model = Libro

class AutorListView(generic.ListView):
	model = Autor
	paginate_by = 3

class AutorDetailView(generic.DetailView):
	model = Autor


from django.contrib.auth.mixins import LoginRequiredMixin

class LibrosPrestadosPorUsuarioListView(LoginRequiredMixin, generic.ListView):
	"""	Vista genérica basada en clases que muestra los libros prestados al usuario actual. """
	model = LibroCopia
	template_name ='catalog/copialibro_lista_prestados_user.html'
	paginate_by = 3

	def get_queryset(self):
		return LibroCopia.objects.filter(prestatario=self.request.user).filter(status__exact='o').order_by('fecha_devolucion')

from django.contrib.auth.mixins import PermissionRequiredMixin

class LibrosPrestadosListView(PermissionRequiredMixin, generic.ListView):
	"""	Vista genérica basada en clases que muestra todos los libros prestados. """
	permission_required = 'catalog.puede_marcar_devuelto'

	model = LibroCopia
	template_name ='catalog/copialibro_lista_prestados.html'
	paginate_by = 3

	def get_queryset(self):
		return LibroCopia.objects.filter(status__exact='o').order_by('fecha_devolucion')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.urls import reverse
# datetime es una biblioteca de Python para manipular fechas y horas. 
import datetime
from .forms import RenovarLibroForm, RenovarLibroModelForm
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.puede_marcar_devuelto')
def RenovarLibroBibliotecario(request, pk):
	# get_object_or_404() Devuelve un objeto especificado de un modelo en función de su valor de clave principal
	# y genera una Http404excepción (no encontrada) si el registro no existe. 
	libro_copia=get_object_or_404(LibroCopia, pk = pk)

	# Si se trata de una solicitud POST, procesa los datos del formulario
	if request.method == 'POST':
		# Crea una instancia de formulario y compléta con datos de la solicitud
		#form = RenovarLibroForm(request.POST)
		form = RenovarLibroModelForm(request.POST)
		# Verifiqua si el formulario es válido
		if form.is_valid():
			# Procesa los datos en form.cleaned_data según sea necesario (aquí solo lo escribimos en el campo modelo fecha_devolucion)
			libro_copia.fecha_devolucion = form.cleaned_data['fecha_devolucion']
			libro_copia.save()

			# HttpResponseRedirect crea una redirección a una URL especificada.
			return HttpResponseRedirect(reverse('prestamos') )

	# Si es un GET (o cualquier otro método), crea el formulario predeterminado.
	else:
		renovar_fecha_por_defecto = datetime.date.today() + datetime.timedelta(weeks=3)
		#form = RenovarLibroForm(initial={'renovar_fecha': renovar_fecha_por_defecto,})
		form = RenovarLibroModelForm(initial={'fecha_devolucion': renovar_fecha_por_defecto,})

	return render(request, 'catalog/libro_renovar_bibliotecario.html', {'form': form, 'librocopia':libro_copia})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Autor

#@permission_required('catalog.puede_marcar_devuelto')
class AutorCreate(PermissionRequiredMixin, CreateView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Autor
	fields = '__all__'
	initial={'fecha_fallecimiento':'05/01/2018',}

class AutorUpdate(PermissionRequiredMixin, UpdateView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Autor
	fields = ['nombre','apellido','fecha_nacimiento','fecha_fallecimiento']

class AutorDelete(PermissionRequiredMixin, DeleteView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Autor
	success_url = reverse_lazy('autores')

class LibroCreate(PermissionRequiredMixin, CreateView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Libro
	fields = '__all__'

class LibroUpdate(PermissionRequiredMixin, UpdateView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Libro
	#fields = ['nombre','apellido','fecha_nacimiento','fecha_fallecimiento']
	fields = '__all__'

class LibroDelete(PermissionRequiredMixin, DeleteView):
	# Se necesita el permiso "catalog.puede_marcar_devuelto" para poder acceder a la vista
	permission_required = 'catalog.puede_marcar_devuelto'
	model = Libro
	success_url = reverse_lazy('libros')