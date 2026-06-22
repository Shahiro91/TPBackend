from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    def decorator(view_func):
        return user_passes_test(
            lambda user: user.is_authenticated and (user.role == role or user.is_superuser),
            login_url='home'
        )(view_func)
    return decorator


def admin_required(view_func):
    return role_required('ADMIN')(view_func)


def profesor_required(view_func):
    return role_required('PROFESOR')(view_func)


def alumno_required(view_func):
    return role_required('ALUMNO')(view_func)
