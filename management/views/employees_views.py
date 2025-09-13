# management/views/employees_views.py
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from management.services.employee_service import EmployeeService
from management.forms.employees_forms import EmployeeForm

nav_link = 'employees'

def employees_list(request):
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  email_query = request.GET.get('email', '')

  result = EmployeeService.get_employees_list(page_number, per_page, search_query, email_query)
  
  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Empleados',
    'employees': result['employees'],
    'search_query': search_query,
    'page': result['page_number'],
    'per_page': result['per_page'],
    'email_query': email_query,
    'total_employees': result['total_employees'],
    'total_pages': result['total_pages'],
    'start_record': result['offset'] + 1,
    'end_record': min(result['offset'] + result['per_page'], result['total_employees']),
  }

  return render(request, 'management/employees/list.html', context)

def delete_employee(request, employee_id):
  if request.method == 'GET':
    success, result = EmployeeService.delete_employee(employee_id)
    
    if success:
      messages.success(request, f'El empleado "{result}" ha sido eliminado correctamente.')
    else:
      messages.error(request, f'Ocurrió un error al intentar eliminar el empleado: {result}')
    
    return redirect('employees_list')
  else:
    return redirect('employees_list')

def create_employee(request):
  context = {"nav_link": nav_link}
  
  if request.method == 'POST':
    form = EmployeeForm(request.POST)
    
    if form.is_valid():
      employee, error = EmployeeService.create_employee(
        form.cleaned_data['names'],
        form.cleaned_data['last_names'],
        form.cleaned_data['document_number'],
        form.cleaned_data['document_type'],
        form.cleaned_data['phone'],
        form.cleaned_data['email'],
        form.cleaned_data['user_id'],
        form.cleaned_data.get('image_url', '/user-default.png')
      )
      
      if error:
        messages.error(request, f'Error al crear en MongoDB: {error}')
        context['form'] = form
        return render(request, 'management/employees/detail.html', context, status=500)
      else:
        messages.success(request, '¡Empleado creado exitosamente!')
        return redirect('employee_detail', employee_id=str(employee.id))
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/employees/detail.html', context, status=400)
  
  context['form'] = EmployeeForm()
  return render(request, 'management/employees/detail.html', context)

def update_employee(request, employee_id):
  employee = EmployeeService.get_employee_by_id(employee_id)
  
  if not employee:
    messages.error(request, 'El empleado no fue encontrado.')
    return redirect('employees_list')

  if request.method == 'POST':
    form = EmployeeForm(request.POST)
    
    if form.is_valid():
      updated_employee, error = EmployeeService.update_employee(
        employee_id,
        form.cleaned_data['names'],
        form.cleaned_data['last_names'],
        form.cleaned_data['document_number'],
        form.cleaned_data['document_type'],
        form.cleaned_data['phone'],
        form.cleaned_data['email'],
        form.cleaned_data['user_id'],
        form.cleaned_data.get('image_url', '/user-default.png')
      )
      
      if error:
        messages.error(request, f'Error al actualizar: {error}')
      else:
        messages.success(request, f'El empleado "{updated_employee.names}" ha sido actualizado correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
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