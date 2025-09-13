from django.shortcuts import redirect
from django.http import JsonResponse
from functools import wraps

def auth_required(view_func):
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):
    print('1+++++++++++++++++++++++++++')
    if request.session.get('authenticated') is not True:
      if request.META.get('HTTP_ACCEPT', '').find('application/json') != -1:
        return JsonResponse({
          "error": "authentication_required",
          "message": "Por favor inicie sesión"
        }, status=401)
      else:
        return redirect('managment_index')  # nombre de la ruta al login
    return view_func(request, *args, **kwargs)
  return wrapper


def auth_required_inverse(view_func):
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):
    if request.session.get('authenticated') is True:
      return redirect('home')  # nombre de la ruta principal
    return view_func(request, *args, **kwargs)
  return wrapper
