from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.employees_forms import EmployeeForm
from mongoengine.errors import DoesNotExist
from management.models.employee import Employee
from management.models.enterprise import Enterprise
from datetime import datetime
import math

nav_link = 'employees'

def employees_list(request):
  # Obtener parámetros de la URL
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  email_query = request.GET.get('email', '') 

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

  # Consultar y filtrar las empresas
  employees = Employee.objects.all()
  # Construir una lista de consultas Q para combinar
  query_list = []
  if search_query:
    query_list.append(Q(names__icontains=search_query) | Q(last_names__icontains=search_query))
  
  if email_query:
    query_list.append(Q(email__icontains=email_query))

  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    employees = employees.filter(combined_query)

  # Lógica de paginación
  total_employees = employees.count()
  total_pages = math.ceil(total_employees / per_page)
  
  # Calcular el offset para la consulta (skip)
  offset = (page_number - 1) * per_page
  
  # Obtener las empresas para la página actual
  paginated_employees = employees.skip(offset).limit(per_page)

  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de empleados',
    'employees': paginated_employees,
    'search_query': search_query,
    'page': page_number,
    'per_page': per_page,
    'email_query': email_query,
    'total_employees': total_employees,
    'total_pages': total_pages,
    'start_record': offset + 1,
    'end_record': min(offset + per_page, total_employees),
  }

  return render(request, 'management/employees/list.html', context)

def delete_employee(request, employee_id):
  if request.method == 'GET':
    try:
      # Usamos el ObjectId para encontrar el documento
      employee = Employee.objects.get(id=ObjectId(employee_id))
      employee.delete()
      messages.success(request, f'El empleado "{employee.names}" ha sido eliminada correctamente.')
    except Employee.DoesNotExist:
      messages.error(request, 'El empleado no fue encontrada.')
    except Exception as e:
      messages.error(request, f'Ocurrió un error al intentar eliminar el empleado: {e}')
    
    return redirect('employees_list')
  else:
    # Si la solicitud no es POST, puedes redirigir o mostrar una página de confirmación
    # Para este ejemplo, simplemente redirigimos de vuelta a la lista
    return redirect('employees_list')

def create_employee(request):
  context = {
    "nav_link": nav_link
  }
  
  if request.method == 'POST':
    form = EmployeeForm(request.POST)
    
    if form.is_valid():
      try:
        # Create a new enterprise with form data
        employee = Employee(
          names=form.cleaned_data['names'],
          last_names=form.cleaned_data['last_names'],
          document_number=form.cleaned_data['document_number'],
          document_type=form.cleaned_data['document_type'],
          phone=form.cleaned_data['phone'],
          email=form.cleaned_data['email'],
          user_id=form.cleaned_data['user_id'],
          image_url=form.clean_image_url(),
        )
        
        # Save to MongoDB
        employee.save()

        # Success message and redirect
        messages.success(request, '¡Empleado creada exitosamente!')
        return redirect('employee_detail', employee_id=str(employee.id))
          
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/employees/detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/employees/detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = EmployeeForm()
  return render(request, 'management/employees/detail.html', context)

def update_employee(request, employee_id):
  """
  Vista para editar una empresa existente usando un forms.Form.
  Maneja la carga del formulario con datos iniciales (GET) y
  el guardado manual de los datos (POST).
  """
  try:
    # 1. Obtener la instancia de la empresa de la base de datos
    employee = Employee.objects.get(id=ObjectId(employee_id))
  except Employee.DoesNotExist:
    messages.error(request, 'El emploeado no fue encontrado.')
    return redirect('employees_list')
  except Exception as e:
    messages.error(request, f'Error al buscar al empleado: {e}')
    return redirect('employees_list')

  if request.method == 'POST':
    # 2. Para POST, inicializar el formulario con los datos enviados
    form = EmployeeForm(request.POST)
    if form.is_valid():
      # 3. Acceder a los datos limpios y actualizar el objeto manualmente
      cleaned_data = form.cleaned_data
      
      # Mapear los campos del formulario a los del modelo
      employee.names = cleaned_data['names']
      employee.last_mames = cleaned_data['last_names']
      employee.document_number = cleaned_data['document_number']
      employee.document_type = cleaned_data['document_type']
      employee.phone = cleaned_data['phone']
      employee.email = cleaned_data['email']
      employee.user_id = cleaned_data['user_id']
      employee.image_url = str(cleaned_data.get('image_url', '/user-default.png')).strip() or '/user-default.png'
      
      # 4. Guardar los cambios en la base de datos
      employee.save() 
      
      messages.success(request, f'El empleado "{employee.names}" ha sido actualizado correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    # 5. Para GET, crear un diccionario con los datos del objeto
    #    y pasar el diccionario al parámetro 'initial'
    initial_data = {
      'id': str(employee.id),
      'names': employee.names,
      'last_names': employee.last_names,
      'document_number': employee.document_number,
      'document_type': employee.document_type,
      'user_id': employee.user_id,
      'email': employee.email,
      'phone': employee.phone,
      'image_url': employee.image_url,
    }
    form = EmployeeForm(initial=initial_data)
  context = {
    'editing': True,
    'form': form,
    'employee': employee,
    'page_title': 'Editar Empleado',
    'nav_link': nav_link, 
  }
  return render(request, 'management/employees/detail.html', context)