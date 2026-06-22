from django.urls import path
from . import views

app_name = 'profesor'

urlpatterns = [
    path('', views.lista_profesores, name='lista_profesores'),
    path('mis-clases/<int:profesor_id>/', views.mis_clases, name='mis_clases'),
    path('mis-clases/<int:profesor_id>/alumnos/<int:clase_id>/', views.alumnos_por_clase, name='alumnos_por_clase'),
    path('crear/', views.crear_profesor, name='crear_profesor'),
]

