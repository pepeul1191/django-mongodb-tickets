import os
import requests
import json

def auth_service_login(username, password):
  """Servicio de autenticación - equivalente al Go service"""
  # Obtener variables de entorno
  url_access = os.getenv('URL_ACCESS_SERVICE')
  x_auth_access = os.getenv('X_AUTH_ACCESS_SERVICE')
  system_id_str = os.getenv('SYSTEM_ID')
  
  if not all([url_access, x_auth_access, system_id_str]):
    raise Exception('Servicio de autenticación no configurado correctamente')
  
  try:
    system_id = int(system_id_str)
  except ValueError:
    raise Exception('Configuración del sistema inválida')
  
  # Preparar el request
  payload = {
    'username': username,
    'password': password,
    'system_id': system_id
  }
  
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Auth-Trigger': x_auth_access
  }
  
  # Realizar la petición
  url = f"{url_access}/api/v1/users/sign-in/by-username"
  
  try:
    response = requests.post(
      url, 
      json=payload, 
      headers=headers,
      timeout=30
    )
    response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx
    
    # Parsear la respuesta
    return response.json()
      
  except requests.exceptions.Timeout:
    raise Exception('Timeout al conectar con el servicio de autenticación')
  except requests.exceptions.ConnectionError:
    raise Exception('No se pudo conectar con el servicio de autenticación')
  except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
      raise Exception('Credenciales inválidas')
    else:
      raise Exception(f'Error del servicio de autenticación: {e.response.status_code}')
  except json.JSONDecodeError:
    raise Exception('Respuesta inválida del servicio de autenticación')