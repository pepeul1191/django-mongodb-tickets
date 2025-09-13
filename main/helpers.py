import os

def custom_urls(request):
  return {
    'BASE_URL_FROM_ENV': os.getenv('BASE_URL'),
    'FILES_URL_FROM_ENV': os.getenv('FILES_URL'),
  }

def custom_auth_status(request):
  return {
    'authenticated': request.session.get('authenticated', False),
    'user': request.session.get('user', {}),
    'roles': request.session.get('roles', []),
  }

def custom_user_has_role(request, role_name):
  roles = request.session.get('roles', [])
  for role in roles:
    if role.get('name') == role_name:
      return True
  return False