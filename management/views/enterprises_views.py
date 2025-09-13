# management/views/enterprises_view.py
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from management.services.enterprise_service import EnterpriseService
from management.forms.enterprises_forms import EnterpriseForm

nav_link = 'enterprises'

def enterprises_list(request):
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  tax_id_query = request.GET.get('tax_id', '')

  result = EnterpriseService.get_enterprises_list(page_number, per_page, search_query, tax_id_query)
  
  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Empresas',
    'enterprises': result['enterprises'],
    'search_query': search_query,
    'page': result['page_number'],
    'per_page': result['per_page'],
    'tax_id_query': tax_id_query,
    'total_enterprises': result['total_enterprises'],
    'total_pages': result['total_pages'],
    'start_record': result['offset'] + 1,
    'end_record': min(result['offset'] + result['per_page'], result['total_enterprises']),
  }

  return render(request, 'management/enterprises/list.html', context)

def delete_enterprise(request, enterprise_id):
  if request.method == 'GET':
    success, result = EnterpriseService.delete_enterprise(enterprise_id)
    
    if success:
      messages.success(request, f'La empresa "{result}" ha sido eliminada correctamente.')
    else:
      messages.error(request, f'Ocurrió un error al intentar eliminar la empresa: {result}')
    
    return redirect('enterprises_list')
  else:
    return redirect('enterprises_list')

def create_enterprise(request):
  context = {"nav_link": nav_link}
  
  if request.method == 'POST':
    form = EnterpriseForm(request.POST)
    
    if form.is_valid():
      enterprise, error = EnterpriseService.create_enterprise(
        form.cleaned_data['business_name'],
        form.cleaned_data['trade_name'],
        form.cleaned_data['tax_id'],
        form.cleaned_data['fiscal_address'],
        form.cleaned_data['location_id'],
        form.cleaned_data['phone'],
        form.cleaned_data['email'],
        form.cleaned_data['website'],
        request.POST.get('image_url', '')
      )
      
      if error:
        messages.error(request, f'Error al crear en MongoDB: {error}')
        context['form'] = form
        return render(request, 'management/enterprises/detail.html', context, status=500)
      else:
        messages.success(request, '¡Empresa creada exitosamente!')
        return redirect('enterprise_detail', enterprise_id=str(enterprise.id))
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/enterprises/detail.html', context, status=400)
  
  context['form'] = EnterpriseForm()
  return render(request, 'management/enterprises/detail.html', context)

def update_enterprise(request, enterprise_id):
  enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
  
  if not enterprise:
    messages.error(request, 'La empresa no fue encontrada.')
    return redirect('enterprises_list')

  location_data = EnterpriseService.get_location_hierarchy(enterprise.location_id)

  if request.method == 'POST':
    form = EnterpriseForm(request.POST)
    
    if form.is_valid():
      updated_enterprise, error = EnterpriseService.update_enterprise(
        enterprise_id,
        form.cleaned_data['business_name'],
        form.cleaned_data['trade_name'],
        form.cleaned_data['tax_id'],
        form.cleaned_data['fiscal_address'],
        form.cleaned_data['location_id'],
        form.cleaned_data['phone'],
        form.cleaned_data['email'],
        form.cleaned_data['website'],
        form.cleaned_data['image_url']
      )
      
      if error:
        messages.error(request, f'Error al actualizar: {error}')
      else:
        messages.success(request, f'La empresa "{updated_enterprise.business_name}" ha sido actualizada correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    initial_data = {
      'id': str(enterprise.id),
      'business_name': enterprise.business_name,
      'trade_name': enterprise.trade_name,
      'tax_id': enterprise.tax_id,
      'phone': enterprise.phone,
      'website': enterprise.website,
      'email': enterprise.email,
      'location_id': str(enterprise.location_id),
      'fiscal_address': enterprise.fiscal_address,
      'image_url': enterprise.image_url,
    }
    form = EnterpriseForm(initial=initial_data)
  
  context = {
    'editing': True,
    'form': form,
    'enterprise': enterprise,
    'page_title': 'Editar Empresa',
    'nav_link': nav_link, 
    'location': location_data
  }
  
  return render(request, 'management/enterprises/detail.html', context)

def employees_enterprise(request, enterprise_id):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      success, error = EnterpriseService.update_enterprise_employees(enterprise_id, data['employees'])
      
      if success:
        return JsonResponse({'message': f'Empleados asociados a la empresa', 'status': 'success'}, status=200)
      else:
        return JsonResponse({'error': error, 'message': 'Error al asociar empleados'}, status=500)
    except Exception as e:
      return JsonResponse({'error': str(e), 'message': 'Error al procesar la solicitud'}, status=500)
  
  else:
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    search_query = request.GET.get('name', '')
    email_query = request.GET.get('email', '') 
    association_status = request.GET.get('association_status', '2')

    result = EnterpriseService.get_enterprise_employees(
      enterprise_id, page_number, per_page, search_query, email_query, association_status
    )
    
    if result is None:
      messages.error(request, 'Error al cargar empleados')
      return redirect('enterprises_list')

    context = {
      'employees': result['employees'],
      'search_query': search_query,
      'email_query': email_query,
      'page': result['page_number'],
      'per_page': result['per_page'],
      'association_status': int(association_status),
      'total_employees': result['total_employees'],
      'total_pages': result['total_pages'],
      'nav_link': nav_link,
      'start_record': result['offset'] + 1,
      'end_record': min(result['offset'] + result['per_page'], result['total_employees']),
      'enterprise_id': enterprise_id,
    }

    return render(request, 'management/enterprises/employees.html', context)

def assets_enterprise(request, enterprise_id):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      success, error = EnterpriseService.update_enterprise_assets(enterprise_id, data['assets'])
      
      if success:
        return JsonResponse({'message': f'Activos asociados a la empresa', 'status': 'success'}, status=200)
      else:
        return JsonResponse({'error': error, 'message': 'Error al asociar activos'}, status=500)
    except Exception as e:
      return JsonResponse({'error': str(e), 'message': 'Error al procesar la solicitud'}, status=500)
  
  else:
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    search_query = request.GET.get('name', '')
    code_query = request.GET.get('code', '') 
    association_status = request.GET.get('association_status', '2')

    result = EnterpriseService.get_enterprise_assets(
      enterprise_id, page_number, per_page, search_query, code_query, association_status
    )
    
    if result is None:
      messages.error(request, 'Error al cargar activos')
      return redirect('enterprises_list')

    context = {
      'assets': result['assets'],
      'search_query': search_query,
      'code_query': code_query,
      'page': result['page_number'],
      'per_page': result['per_page'],
      'association_status': int(association_status),
      'total_assets': result['total_assets'],
      'total_pages': result['total_pages'],
      'nav_link': nav_link,
      'start_record': result['offset'] + 1,
      'end_record': min(result['offset'] + result['per_page'], result['total_assets']),
      'enterprise_id': enterprise_id,
    }

    return render(request, 'management/enterprises/assets.html', context)