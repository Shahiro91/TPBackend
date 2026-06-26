from django.urls import path
from . import views

# Nombre del espacio de URLs de esta app
app_name = 'profesor'

urlpatterns = [


    path('crear/', views.crear_profesor, name='crear_profesor'),
    path('editar-perfil/<int:profesor_id>/', views.editar_perfil, name='editar_perfil'),    

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
