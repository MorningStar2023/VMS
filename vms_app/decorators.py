from django.shortcuts import redirect
from functools import wraps


def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('no_access_page')

    return wrapper


def active_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('not_authorised')

    return wrapper
