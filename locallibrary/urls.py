from django.contrib import admin
from django.urls import path, include

# Agrega mapeo de URL para redirigir la URL base a la aplicación
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Use static() para agregar mapeo de URL para servir archivos estáticos durante el desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
