"""catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls import url

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('libros/', views.LibroListView.as_view(), name='libros'),
	path('libro/<int:pk>/', views.LibroDetailView.as_view(), name='libro-detalle'),
	path('autores/', views.AutorListView.as_view(), name='autores'),
	path('autor/<int:pk>/', views.AutorDetailView.as_view(), name='autor-detalle'),   
]

# URLConf para listr los libros prestados por usuario y en general.
urlpatterns += [
    path('mislibros/', views.LibrosPrestadosPorUsuarioListView.as_view(), name='mis-prestamos'),
    path('prestamos/', views.LibrosPrestadosListView.as_view(), name='prestamos'),
]

# URLConf para renovar (fecha_devolucion) un libro.
urlpatterns += [
    path('libro/<uuid:pk>/renovar/', views.RenovarLibroBibliotecario, name='renovar-libro-bibliotecario'),
]

# URLConf para crear, actualizar y eliminar autores
urlpatterns += [
    path('autor/create/', views.AutorCreate.as_view(), name='autor_create'),
    path('autor/<int:pk>/update/', views.AutorUpdate.as_view(), name='autor_update'),
    path('autor/<int:pk>/delete/', views.AutorDelete.as_view(), name='autor_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('libro/create/', views.LibroCreate.as_view(), name='libro_create'),
    path('libro/<int:pk>/update/', views.LibroUpdate.as_view(), name='libro_update'),
    path('libro/<int:pk>/delete/', views.LibroDelete.as_view(), name='libro_delete'),
]