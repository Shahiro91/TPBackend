from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.utils import generate_unique_email

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == user.ADMIN or user.is_superuser:
                return redirect('admin_panel')
            if user.role == user.PROFESOR:
                return redirect('profesor:mis_clases', profesor_id=user.profesor.id)
            if user.alumno_id:
                return redirect('alumno:dashboard')
            return redirect('alumno:lista_alumnos')
        messages.error(request, 'Correo o contraseña inválidos.')
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_redirect(request):
    if request.user.role == request.user.ADMIN or request.user.is_superuser:
        return redirect('admin_panel')
    if request.user.role == request.user.PROFESOR:
        return redirect('profesor:mis_clases', profesor_id=request.user.profesor.id)
    if request.user.alumno_id:
        return redirect('alumno:dashboard')
    return redirect('alumno:lista_alumnos')


@login_required(login_url='home')
def crear_administrativo(request):
    # Solo superusuarios pueden crear administrativos
    if not request.user.is_superuser:
        messages.error(request, 'No tenés permiso para crear administrativos.')
        return redirect('admin_panel')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password')
        
        if not first_name or not last_name or not password:
            messages.error(request, 'Nombre, apellido y contraseña son obligatorios.')
            return redirect('admin_panel')
        
        # Genera email automático (mismo formato que Alumno y Profesor)
        email = generate_unique_email(first_name, last_name)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'El email {email} ya existe. Intente con otro nombre.')
            return redirect('admin_panel')
        
        # Crea usuario con rol ADMIN (is_staff=False, is_superuser=False)
        User.objects.create_user(
            email=email,
            password=password,
            role=User.ADMIN,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_superuser=False,
        )
        messages.success(request, f'Administrativo creado correctamente. Email: {email} / Contraseña: {password}')
        return redirect('admin_panel')
    
    return redirect('admin_panel')