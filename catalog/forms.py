from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
    
class RenovarLibroForm(forms.Form):
	renovar_fecha = forms.DateField(help_text="Inrese una fecha entre hoy y 4 semanas siguientes (por defecto son 3).")

	def clean_renovar_fecha_devolucion(self):
		data = self.cleaned_data['renovar_fecha']

		# Verificamos que la fecha no este en el pasado.
		if data < datetime.date.today():
			raise ValidationError(_('Fecha no válida - renovación en el pasado'))

		# Verificamos que la fecha este en el rango que el bibliotecario puede cambiar (+4 semanas).
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Fecha no válida - renovación con más de 4 semanas de anticipación'))

		# Recuerde devolver siempre los datos limpios.
		return data

from django.forms import ModelForm
from .models import LibroCopia

class RenovarLibroModelForm(ModelForm):
	def clean_fecha_devolucion(self):
		data = self.cleaned_data['fecha_devolucion']

		# Verifica si la fecha_devolucion no está pasada.
		if data < datetime.date.today():
			raise ValidationError(_('Fecha no válida - renovación en el pasado.'))

		# Verifica si la fecha_devolucion esta en el rango permitido, maximo 4 semanas.
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Fecha no válida - renovación maximo por 4 semanas.'))

		# Remember to always return the cleaned data.
		return data
	class Meta:
		model = LibroCopia
		fields = ['fecha_devolucion',]
		labels = { 'fecha_devolucion': _('Nueva fecha de devolcuon'), }
		help_texts = { 'fecha_devolucion': _('Inrese una fecha entre hoy y 4 semanas siguientes (por defecto son 3).'), }