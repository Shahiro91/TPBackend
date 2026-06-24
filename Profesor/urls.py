from django.urls import path
from . import views

# Nombre del espacio de URLs de esta app
app_name = 'profesor'

urlpatterns = [
    # URL principal del módulo, muestra el listado de todos los profesores
    path('', views.lista_profesores, name='lista_profesores'),

    # URL para crear un nuevo profesor
    path('crear/', views.crear_profesor, name='crear_profesor'),

    # URL para ver las clases asignadas a un profesor específico
    path(
        'mis-clases/<int:profesor_id>/',
        views.mis_clases,
        name='mis_clases'
    ),

    # URL para ver los alumnos de una clase específica de un profesor
    path(
        'mis-clases/<int:profesor_id>/alumnos/<int:clase_id>/',
        views.alumnos_por_clase,
        name='alumnos_por_clase'
    ),
]
