from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import profesor_required
from .models import Profesor
from Clase.models import Clase

# Muestra las clases asignadas a un profesor específico
@login_required(login_url='home')
@profesor_required
def mis_clases(request, profesor_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    clases = profesor.clases.all()
    q = request.GET.get('q')
    if q:
        clases = clases.filter(nombre__icontains=q)
    return render(request, 'mis_clases_profesor.html', {
        'profesor': profesor,
        'clases': clases,
    })

# Muestra los alumnos de una clase específica de un profesor
@login_required(login_url='home')
@profesor_required
def alumnos_por_clase(request, profesor_id, clase_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = clase.alumnos.all()
    q = request.GET.get('q')
    if q:
        alumnos = alumnos.filter(nombre__icontains=q)
    return render(request, 'alumnos_por_clase.html', {
        'profesor': profesor,
        'clase': clase,
        'alumnos': alumnos,
    })

# Muestra el listado completo de profesores
@login_required(login_url='home')
@profesor_required
def lista_profesores(request):
    profesores = Profesor.objects.all()
    q = request.GET.get('q')
    if q:
        profesores = profesores.filter(nombre__icontains=q)
    return render(request, 'lista_profesores.html', {
        'profesores': profesores,
    })

@login_required(login_url='home')
@profesor_required
def crear_profesor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        clases_ids = request.POST.getlist('clases')

        if not nombre or not apellido:
            messages.error(request, 'Nombre y apellido son obligatorios.')
            clases = Clase.objects.all()
            return render(request, 'crear_profesor.html', {'clases': clases, 'nombre': nombre, 'apellido': apellido})

        profesor = Profesor.objects.create(nombre=nombre, apellido=apellido)
        if clases_ids:
            profesor.clases.set(clases_ids)
        messages.success(request, 'Profesor creado correctamente.')
        return redirect('admin_panel')

    clases = Clase.objects.all()
    return render(request, 'crear_profesor.html', {'clases': clases})

