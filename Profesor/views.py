from django.shortcuts import render, get_object_or_404
from .models import Profesor
from Clase.models import Clase

# Muestra las clases asignadas a un profesor específico
def mis_clases(request, profesor_id):
    # Busca el profesor por su id, si no existe devuelve error 404
    profesor = get_object_or_404(Profesor, id=profesor_id)
    # Trae todas las clases asociadas a ese profesor
    clases = profesor.clases.all()
    # Renderiza el template enviando el profesor y sus clases
    return render(request, 'mis_clases_profesor.html', {
        'profesor': profesor,
        'clases': clases,
    })

# Muestra los alumnos de una clase específica de un profesor
def alumnos_por_clase(request, profesor_id, clase_id):
    # Busca el profesor por su id, si no existe devuelve error 404
    profesor = get_object_or_404(Profesor, id=profesor_id)
    # Busca la clase por su id, si no existe devuelve error 404
    clase = get_object_or_404(Clase, id=clase_id)
    # Trae todos los alumnos inscriptos en esa clase
    alumnos = clase.alumnos.all()
    # Captura el texto ingresado en el buscador (viene por GET en la URL)
    q = request.GET.get('q')
    if q:
        # Filtra los alumnos cuyo nombre contenga ese texto (icontains significa que no distingue entre mayúsculas y minúsculas)
        alumnos = alumnos.filter(nombre__icontains=q)
    # Renderiza el template enviando el profesor, la clase y los alumnos
    return render(request, 'alumnos_por_clase.html', {
        'profesor': profesor,
        'clase': clase,
        'alumnos': alumnos,
    })

# Muestra el listado completo de profesores
def lista_profesores(request):
    # Trae todos los profesores de la base de datos
    profesores = Profesor.objects.all()
    # Captura el texto ingresado en el buscador (viene por GET en la URL)
    q = request.GET.get('q')
    if q:
        # Filtra los profesores cuyo nombre contenga ese texto
        profesores = profesores.filter(nombre__icontains=q)
    # Renderiza el template enviando la lista de profesores
    return render(request, 'lista_profesores.html', {
        'profesores': profesores,
    })

