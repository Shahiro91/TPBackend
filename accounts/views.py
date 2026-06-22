from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse


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
                return redirect('profesor:lista_profesores')
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
        return redirect('profesor:lista_profesores')
    return redirect('alumno:lista_alumnos')
