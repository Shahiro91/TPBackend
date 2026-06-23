from django.contrib import admin
from django.urls import include, path
from Alumno import views as alumno_views
from . import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('clases/', include('Clase.urls')),
    path('profesores/', include('Profesor.urls')),
    path('planes/', include('Plan.urls')),
    path('alumnos/', include('Alumno.urls')),
    path('mi-admin/', alumno_views.admin_panel, name='admin_panel'),
    path('', core_views.index, name='home'),
]
