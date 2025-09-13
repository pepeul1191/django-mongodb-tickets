from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from main.services import auth_service_login
from .decorators import auth_required, auth_required_inverse
import logging

logger = logging.getLogger(__name__)

def index(request):
  context = {
    'page_title': 'Página Principal',
    'items': ['Item 1', 'Item 2', 'Item 3']
  }
  return render(request, 'main/index.html', context)

@auth_required_inverse
def sing_in(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    # Validar campos vacíos
    if not username or not password:
      messages.error(request, 'Campos no pueden estar vacíos')
      return redirect('sign_in')
  
    try:
      # Llamar al servicio de autenticación
      response_data = auth_service_login(username, password)
      
      if response_data.get('success'):
        # Login exitoso
        request.session['user'] = response_data['data']['user']
        request.session['roles'] = response_data['data']['roles']
        request.session['authenticated'] = True
        messages.success(request, '¡Login exitoso!')
        return redirect('managment_index')
      else:
        # Login fallido
        messages.error(request, response_data.get('message', 'Error de autenticación'))
        return redirect('sign_in')
            
    except Exception as e:
      logger.error(f"Error en login: {str(e)}")
      messages.error(request, str(e))
      return redirect('sign_in')
  else:
    context = {}
    return render(request, 'main/sign-in.html', context)

def sing_out(request):
  storage = messages.get_messages(request)
  storage.used = True  # Esto marca todos los mensajes como usados/eliminados
  
  # Limpiar la sesión actual
  request.session.flush()
  
  # Agregar solo el nuevo mensaje
  messages.success(request, 'Sesión cerrada')
  
  return redirect('sign_in')

def profile(request):
  user = request.session.get('user', {})
  roles = request.session.get('roles', [])
  authenticated = request.session.get('authenticated', False)

  return JsonResponse({
    'user': user,
    'roles': roles,
    'authenticated': authenticated
  })

def reset_password(request):
  context = {}
  return render(request, 'main/reset-password.html', context)

def handler404(request, exception):
  return render(request, '404.html', {}, status=404)