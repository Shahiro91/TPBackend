from django.urls import path
from . import views

app_name= 'alumno'

urlpatterns = [
    path('', views.lista_alumnos, name='lista_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('mis-clases/<int:alumno_id>/', views.mis_clases, name='mis_clases'),
    path('mis-reclamos/<int:alumno_id>/', views.mis_reclamos, name='mis_reclamos'),
    path('crear-reclamo/<int:alumno_id>/', views.crear_reclamo, name='crear_reclamo'),
    path('dashboard/<int:alumno_id>/', views.dashboard_alumno, name='dashboard'),
]
