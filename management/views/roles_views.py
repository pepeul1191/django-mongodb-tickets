from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.roles_forms import RoleForm
from management.models.role import Role
import math

from management.models.location import Location

nav_link = 'roles'

def roles_list(request):
  # Obtener parámetros de la URL
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')

  # Validar y convertir a enteros
  try:
    page_number = int(page_number)
    per_page = int(per_page)
  except (ValueError, TypeError):
    page_number = 1
    per_page = 10
  
  # Validar que no sean valores negativos o cero
  if page_number < 1:
    page_number = 1
  if per_page < 1:
    per_page = 10

  # Consultar y filtrar El rols
  roles = Role.objects.all()
  # Construir una lista de consultas Q para combinar
  query_list = []
  if search_query:
    query_list.append(Q(name__icontains=search_query))
  

  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    roles = roles.filter(combined_query)

  # Lógica de paginación
  total_roles = roles.count()
  total_pages = math.ceil(total_roles / per_page)
  
  # Calcular el offset para la consulta (skip)
  offset = (page_number - 1) * per_page
  
  # Obtener El rols para la página actual
  paginated_roles = roles.skip(offset).limit(per_page)

  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Roles',
    'roles': paginated_roles,
    'search_query': search_query,
    'page': page_number,
    'per_page': per_page,
    'total_roles': total_roles,
    'total_pages': total_pages,
    'start_record': offset + 1,
    'end_record': min(offset + per_page, total_roles),
  }

  return render(request, 'management/roles/list.html', context)

def delete_role(request, role_id):
  if request.method == 'GET':
    try:
      # Usamos el ObjectId para encontrar el documento
      role = Role.objects.get(id=ObjectId(role_id))
      role.delete()
      messages.success(request, f'El rol "{role.name}" ha sido eliminada correctamente.')
    except role.DoesNotExist:
      messages.error(request, 'El rol no fue encontrada.')
    except Exception as e:
      messages.error(request, f'Ocurrió un error al intentar eliminar el rol: {e}')
    
    return redirect('roles_list')
  else:
    # Si la solicitud no es POST, puedes redirigir o mostrar una página de confirmación
    # Para este ejemplo, simplemente redirigimos de vuelta a la lista
    return redirect('roles_list')

def create_role(request):
  context = {}
  
  if request.method == 'POST':
    form = RoleForm(request.POST)
    
    if form.is_valid():
      try:
        # Create a new role with form data
        role = Role(
          name=form.cleaned_data['name'],
          description=form.cleaned_data['description'],  # File upload field
        )
        
        # Save to MongoDB
        role.save()

        # Success message and redirect
        messages.success(request,'¡Rol creado exitosamente!')
        return redirect('role_detail', role_id=str(role.id))
          
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/roles/detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/roles/detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = RoleForm()
  return render(request, 'management/roles/detail.html', context)

def update_role(request, role_id):
  """
  Vista para editar El rol existente usando un forms.Form.
  Maneja la carga del formulario con datos iniciales (GET) y
  el guardado manual de los datos (POST).
  """
  try:
    # 1. Obtener la instancia de El rol de la base de datos
    role = Role.objects.get(id=ObjectId(role_id))
  except role.DoesNotExist:
    messages.error(request, 'El rol no fue encontrada.')
    return redirect('roles_list')
  except Exception as e:
    messages.error(request, f'Error al buscar El rol: {e}')
    return redirect('roles_list')

  if request.method == 'POST':
    # 2. Para POST, inicializar el formulario con los datos enviados
    form = RoleForm(request.POST)
    if form.is_valid():
      # 3. Acceder a los datos limpios y actualizar el objeto manualmente
      cleaned_data = form.cleaned_data
      
      # Mapear los campos del formulario a los del modelo
      role.name = cleaned_data['name']
      role.description = cleaned_data['description']
      
      # 4. Guardar los cambios en la base de datos
      role.save() 
      
      messages.success(request, f'El rol "{role.name}" ha sido actualizadaocorrectamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    # 5. Para GET, crear un diccionario con los datos del objeto
    #    y pasar el diccionario al parámetro 'initial'
    initial_data = {
      'id': str(role.id),
      'name': role.name,
      'description': role.description,
    }
    form = RoleForm(initial=initial_data)
  context = {
    'editing': True,
    'form': form,
    'role': role,
    'page_title': 'Editar Rol',
    'nav_link': nav_link, 
  }
  return render(request, 'management/roles/detail.html', context)