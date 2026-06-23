import re
import unicodedata

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from accounts.decorators import admin_required, alumno_required
from Alumno.forms import AlumnoCreateForm
from Alumno.models import Alumno
from Clase.models import Clase
from Plan.models import Plan
from Profesor.models import Profesor
from Reclamos.models import Reclamos
from django.core.paginator import Paginator

User = get_user_model()

def normalize_name(value):
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '.', value).strip('.')
    return value.lower()


def generate_unique_email(nombre, apellido):
    base = f"{normalize_name(nombre)}.{normalize_name(apellido)}"
    email = f"{base}@centergym.com"
    suffix = 0
    while User.objects.filter(email=email).exists():
        suffix += 1
        email = f"{base}{suffix}@centergym.com"
    return email


ALUMNOS_POR_PAGINA = 6


def lista_alumnos(request):
    q = request.GET.get('q', '').strip()
    alumnos = Alumno.objects.all()

    if q:
        filtros = Q(nombre__icontains=q) | Q(apellido__icontains=q)
        if q.isdigit():
            filtros |= Q(DNI=int(q))
        alumnos = alumnos.filter(filtros)

    return render(request, 'listaAlumnos.html', {'alumnos': alumnos, 'q': q})

@login_required(login_url='home')
@alumno_required
def dashboard_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    # Aquí puedes calcular las clases asignadas si lo necesitas en el futuro
    total_clases = alumno.clases.count() 
    
    return render(request, 'dashboard_alumno.html', {
        'alumno': alumno,
        'total_clases': total_clases,
    })

@login_required(login_url='home')
@admin_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoCreateForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = generate_unique_email(nombre, apellido)

            try:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        email=email,
                        password='alumno',
                        role=User.ALUMNO,
                        first_name=nombre,
                        last_name=apellido,
                    )

                    alumno = form.save()
                    usuario.alumno = alumno
                    usuario.save()

                messages.success(
                    request,
                    f'Alumno creado correctamente. Email: {email} / Contraseña inicial: alumno'
                )
                return redirect('admin_panel')
            except Exception as exc:
                messages.error(request, 'Error al crear el alumno. Por favor revise los datos e intente nuevamente.')
                form.add_error(None, str(exc))
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = AlumnoCreateForm()

    return render(request, 'crear_alumno.html', {'form': form})


@login_required(login_url='home')
@admin_required
def admin_panel(request):
    active_tab = request.GET.get('tab', 'clientes')
    show_plan_form = False
    plan_form = {}
    plan_edit_id = None
    show_clase_form = False
    clase_form = {}
    clase_edit_id = None
    show_profesor_form = False
    profesor_form = {'clases_ids': []}
    profesor_edit_id = None
    show_alumno_form = False
    alumno_form = {'clases_ids': []}
    alumno_edit_id = None

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'editar_alumno':
            active_tab = 'clientes'
            show_alumno_form = True
            alumno_edit_id = request.POST.get('alumno_id') or None
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            dni = request.POST.get('DNI', '').strip()
            monto_deuda = request.POST.get('MontoDeuda', '0').strip() or '0'
            clases_ids = request.POST.getlist('clases')
            alumno_form = {
                'nombre': nombre,
                'apellido': apellido,
                'DNI': dni,
                'MontoDeuda': monto_deuda,
                'clases_ids': [int(c) for c in clases_ids if c.isdigit()],
            }

            if not nombre or not apellido or not dni:
                messages.error(request, 'Nombre, apellido y DNI son obligatorios.')
            else:
                try:
                    dni_int = int(dni)
                    monto_deuda_decimal = float(monto_deuda)
                except ValueError:
                    messages.error(request, 'DNI y deuda deben ser números válidos.')
                else:
                    if alumno_edit_id:
                        alumno = get_object_or_404(Alumno, pk=alumno_edit_id)
                        alumno.nombre = nombre
                        alumno.apellido = apellido
                        alumno.DNI = dni_int
                        alumno.MontoDeuda = monto_deuda_decimal
                        alumno.save()
                        alumno.clases.set(alumno_form['clases_ids'])
                        messages.success(request, 'Cliente actualizado correctamente.')
                        return redirect(f"{request.path}?tab=clientes")

        elif action in ('crear_plan', 'editar_plan'):
            active_tab = 'planes'
            show_plan_form = True
            plan_edit_id = request.POST.get('plan_id') or None
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            precio = request.POST.get('precio', '').strip()
            duracion = request.POST.get('duracion', '').strip()
            plan_form = {
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'duracion': duracion,
            }

            if not nombre or not precio or not duracion:
                messages.error(request, 'Nombre, precio y duración son obligatorios.')
            else:
                try:
                    precio_decimal = float(precio)
                except ValueError:
                    messages.error(request, 'El precio debe ser un número válido.')
                else:
                    if action == 'editar_plan' and plan_edit_id:
                        plan = get_object_or_404(Plan, pk=plan_edit_id)
                        plan.nombre = nombre
                        plan.descripcion = descripcion
                        plan.precio = precio_decimal
                        plan.duracion = duracion
                        plan.save()
                        messages.success(request, 'Plan actualizado correctamente.')
                    else:
                        Plan.objects.create(
                            nombre=nombre,
                            descripcion=descripcion,
                            precio=precio_decimal,
                            duracion=duracion,
                        )
                        messages.success(request, 'Plan creado correctamente.')
                    return redirect(f"{request.path}?tab=planes")

        elif action in ('crear_clase', 'editar_clase'):
            active_tab = 'clases'
            show_clase_form = True
            clase_edit_id = request.POST.get('clase_id') or None
            nombre = request.POST.get('nombre', '').strip()
            dias = request.POST.get('dias', '').strip()
            horario = request.POST.get('horario', '').strip()
            clase_form = {'nombre': nombre, 'dias': dias, 'horario': horario}

            if not nombre:
                messages.error(request, 'El nombre de la clase es obligatorio.')
            else:
                if action == 'editar_clase' and clase_edit_id:
                    clase = get_object_or_404(Clase, pk=clase_edit_id)
                    clase.nombre = nombre
                    clase.dias = dias
                    clase.horario = horario
                    clase.save()
                    messages.success(request, 'Clase actualizada correctamente.')
                else:
                    Clase.objects.create(nombre=nombre, dias=dias, horario=horario)
                    messages.success(request, 'Clase creada correctamente.')
                return redirect(f"{request.path}?tab=clases")

        elif action == 'eliminar_clase':
            active_tab = 'clases'
            clase_id = request.POST.get('clase_id')
            if clase_id:
                clase = get_object_or_404(Clase, pk=clase_id)
                nombre = clase.nombre
                clase.delete()
                messages.success(request, f'Clase "{nombre}" eliminada correctamente.')
            return redirect(f"{request.path}?tab=clases")

        elif action in ('crear_profesor', 'editar_profesor'):
            active_tab = 'profesores'
            show_profesor_form = True
            profesor_edit_id = request.POST.get('profesor_id') or None
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            clases_ids = request.POST.getlist('clases')
            profesor_form = {
                'nombre': nombre,
                'apellido': apellido,
                'clases_ids': [int(c) for c in clases_ids if c.isdigit()],
            }

            if not nombre or not apellido:
                messages.error(request, 'Nombre y apellido son obligatorios.')
            else:
                if action == 'editar_profesor' and profesor_edit_id:
                    profesor = get_object_or_404(Profesor, pk=profesor_edit_id)
                    profesor.nombre = nombre
                    profesor.apellido = apellido
                    profesor.save()
                    profesor.clases.set(profesor_form['clases_ids'])
                    messages.success(request, 'Profesor actualizado correctamente.')
                else:
                    profesor = Profesor.objects.create(nombre=nombre, apellido=apellido)
                    profesor.clases.set(profesor_form['clases_ids'])
                    messages.success(request, 'Profesor creado correctamente.')
                return redirect(f"{request.path}?tab=profesores")

    q_alumnos = request.GET.get('q', '').strip()
    alumnos_qs = Alumno.objects.prefetch_related('clases')

    if q_alumnos:
        filtros = Q(nombre__icontains=q_alumnos) | Q(apellido__icontains=q_alumnos)
        if q_alumnos.isdigit():
            filtros |= Q(DNI=int(q_alumnos))
        alumnos_qs = alumnos_qs.filter(filtros)

    alumnos_paginator = Paginator(alumnos_qs, ALUMNOS_POR_PAGINA)
    alumnos = alumnos_paginator.get_page(request.GET.get('page'))

    clases = Clase.objects.prefetch_related('alumnos').all()
    profesores = Profesor.objects.prefetch_related('clases').all()
    planes = Plan.objects.all()
    reclamos = Reclamos.objects.all()

    context = {
        'alumnos': alumnos,
        'alumnos_total': alumnos_paginator.count,
        'clases': clases,
        'profesores': profesores,
        'planes': planes,
        'reclamos': reclamos,
        'q_alumnos': q_alumnos,
        'active_tab': active_tab,
        'show_plan_form': show_plan_form,
        'plan_form': plan_form,
        'plan_edit_id': plan_edit_id,
        'show_clase_form': show_clase_form,
        'clase_form': clase_form,
        'clase_edit_id': clase_edit_id,
        'show_profesor_form': show_profesor_form,
        'profesor_form': profesor_form,
        'profesor_edit_id': profesor_edit_id,
        'show_alumno_form': show_alumno_form,
        'alumno_form': alumno_form,
        'alumno_edit_id': alumno_edit_id,
    }

    return render(request, 'admin.html', context)

@login_required(login_url='home')
@alumno_required
def mis_clases(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    clases = alumno.clases.all()

    q = request.GET.get('q')
    if q:
        clases = clases.filter(nombre__icontains=q)

    return render(request, 'mis_clases.html', {
        'alumno': alumno,
        'clases': clases,
    })


@login_required(login_url='home')
@alumno_required
def mis_reclamos(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    reclamos = alumno.reclamos.all().order_by('-fecha_reclamo')

    return render(request, 'mis_reclamos.html', {
       'alumno': alumno,
       'reclamos': reclamos,
    })


@login_required(login_url='home')
@alumno_required
def crear_reclamo(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            Reclamos.objects.create(
                alumno=alumno,
                contenido=contenido,
                estado='Pendiente'
            )
            messages.success(request, 'Reclamo enviado correctamente.')
            return redirect('alumno:mis_reclamos', alumno_id=alumno.id)
        else:
            messages.error(request, 'el contenido del reclamo no puede estar vacio.')

    return render(request, 'crear_reclamo.html', {'alumno': alumno})
