from django.urls import path
from . import views

app_name= 'alumno'

urlpatterns = [
    path('', views.lista_alumnos, name='lista_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('mis-clases/', views.mis_clases, name='mis_clases'),
    path('mis-reclamos/', views.mis_reclamos, name='mis_reclamos'),
    path('crear-reclamo/', views.crear_reclamo, name='crear_reclamo'),
    path('dashboard/', views.dashboard_alumno, name='dashboard'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]