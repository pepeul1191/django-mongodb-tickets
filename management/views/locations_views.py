# management/views/locations_view.py
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from management.services.location_service import LocationService
from management.forms.locations_forms import LocationForm

nav_link = 'locations'

def locations(request):
  if request.method == 'GET':
    departments = LocationService.get_departments()
    
    context = {
      'page_title': 'Gestión de Locaciones',
      'nav_link': nav_link,
      'departments': departments,
      'provinces': None,
      'districts': None,
    }
    return render(request, 'management/locations/index.html', context)
  
  return JsonResponse({'status': 'error', 'errors': 'Método no permitido'}, status=400)

def locations_provinces(request, department_id):
  departments = LocationService.get_departments()
  department = LocationService.get_location_by_id(department_id)
  
  if not department:
    raise Http404("Departamento no encontrado")
  
  provinces = LocationService.get_provinces_by_department(department_id)
  
  context = {
    'nav_link': nav_link,
    'departments': departments,
    'department': department,
    'provinces': provinces,
    'districts': None,
    'page_title': f'Provincias de {department.name}'
  }
  return render(request, 'management/locations/index.html', context)

def locations_districts(request, department_id, province_id):
  departments = LocationService.get_departments()
  department = LocationService.get_location_by_id(department_id)
  province = LocationService.get_location_by_id(province_id)
  
  if not department or not province:
    raise Http404("Ubicación no encontrada")
  
  provinces = LocationService.get_provinces_by_department(department_id)
  districts = LocationService.get_districts_by_province(province_id)
  
  context = {
    'nav_link': nav_link,
    'departments': departments,
    'department': department,
    'provinces': provinces,
    'province': province,
    'districts': districts,
    'page_title': f'Distritos de {province.name}'
  }
  return render(request, 'management/locations/index.html', context)

def departments(request):
  context = {'nav_link': nav_link}
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      location, error = LocationService.create_location(
        form.cleaned_data['name'],
        'department'
      )
      if error:
        messages.error(request, f'Error: {error}')
      else:
        messages.success(request, 'Departamento creado exitosamente')
        return redirect('locations')
    else:
      messages.error(request, 'Formulario inválido')
    
    context['form'] = form
    return render(request, 'management/locations/departments.html', context)
  
  return render(request, 'management/locations/departments.html', context)

def departments_edit(request, department_id):
  department = LocationService.get_location_by_id(department_id)
  if not department:
    raise Http404("Departamento no encontrado")
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      _, error = LocationService.update_location(
        department_id,
        form.cleaned_data['name']
      )
      if error:
        messages.error(request, f'Error: {error}')
      else:
        messages.success(request, 'Departamento actualizado')
        return redirect('locations')
    else:
      messages.error(request, 'Formulario inválido')
    
    return render(request, 'management/locations/departments.html', {
      'nav_link': nav_link,
      'editing': True,
      'form': form
    })
  
  form = LocationForm(initial={'name': department.name, 'id': department.id})
  return render(request, 'management/locations/departments.html', {
    'nav_link': nav_link,
    'editing': True,
    'form': form
  })

def departments_delete(request, department_id):
  success, error = LocationService.delete_location(department_id)
  if error:
    messages.error(request, f'Error: {error}')
  else:
    messages.success(request, 'Departamento eliminado')
  return redirect('locations')

def provinces_add(request, department_id):
  department = LocationService.get_location_by_id(department_id)
  if not department:
    raise Http404("Departamento no encontrado")
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      is_valid, error = LocationService.validate_parent_child_relationship(
        department_id, 'province'
      )
      if not is_valid:
        messages.error(request, error)
      else:
        location, error = LocationService.create_location(
          form.cleaned_data['name'],
          'province',
          department_id
        )
        if error:
          messages.error(request, f'Error: {error}')
        else:
          messages.success(request, 'Provincia creada')
          return redirect('locations_provinces', department_id=department_id)
    else:
      messages.error(request, 'Formulario inválido')
    
    return render(request, 'management/locations/provinces.html', {
      'nav_link': nav_link,
      'department': department,
      'form': form
    })
  
  return render(request, 'management/locations/provinces.html', {
    'nav_link': nav_link,
    'department': department
  })

def provinces_edit(request, department_id, province_id):
  department = LocationService.get_location_by_id(department_id)
  province = LocationService.get_location_by_id(province_id)
  
  if not department or not province:
    raise Http404("Ubicación no encontrada")
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      _, error = LocationService.update_location(
        province_id,
        form.cleaned_data['name']
      )
      if error:
        messages.error(request, f'Error: {error}')
      else:
        messages.success(request, 'Provincia actualizada')
        return redirect('locations_provinces', department_id=department_id)
    else:
      messages.error(request, 'Formulario inválido')
    
    return render(request, 'management/locations/provinces.html', {
      'nav_link': nav_link,
      'department': department,
      'province': province,
      'editing': True,
      'form': form
    })
  
  form = LocationForm(initial={'name': province.name})
  return render(request, 'management/locations/provinces.html', {
    'nav_link': nav_link,
    'department': department,
    'province': province,
    'editing': True,
    'form': form
  })

def provinces_delete(request, department_id, province_id):
  success, error = LocationService.delete_location(province_id)
  if error:
    messages.error(request, f'Error: {error}')
  else:
    messages.success(request, 'Provincia eliminada')
  return redirect('locations_provinces', department_id=department_id)

def districts_add(request, department_id, province_id):
  department = LocationService.get_location_by_id(department_id)
  province = LocationService.get_location_by_id(province_id)
  
  if not department or not province:
    raise Http404("Ubicación no encontrada")
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      is_valid, error = LocationService.validate_parent_child_relationship(
        province_id, 'district'
      )
      if not is_valid:
        messages.error(request, error)
      else:
        location, error = LocationService.create_location(
          form.cleaned_data['name'],
          'district',
          province_id
        )
        if error:
          messages.error(request, f'Error: {error}')
        else:
          messages.success(request, 'Distrito creado')
          return redirect('locations_districts', department_id=department_id, province_id=province_id)
    else:
      messages.error(request, 'Formulario inválido')
    
    return render(request, 'management/locations/districts.html', {
      'nav_link': nav_link,
      'department': department,
      'province': province,
      'form': form
    })
  
  return render(request, 'management/locations/districts.html', {
    'nav_link': nav_link,
    'department': department,
    'province': province
  })

def districts_edit(request, department_id, province_id, district_id):
  department = LocationService.get_location_by_id(department_id)
  province = LocationService.get_location_by_id(province_id)
  district = LocationService.get_location_by_id(district_id)
  
  if not department or not province or not district:
    raise Http404("Ubicación no encontrada")
  
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      _, error = LocationService.update_location(
        district_id,
        form.cleaned_data['name']
      )
      if error:
        messages.error(request, f'Error: {error}')
      else:
        messages.success(request, 'Distrito actualizado')
        return redirect('locations_districts', department_id=department_id, province_id=province_id)
    else:
      messages.error(request, 'Formulario inválido')
    
    return render(request, 'management/locations/districts.html', {
      'nav_link': nav_link,
      'department': department,
      'province': province,
      'district': district,
      'editing': True,
      'form': form
    })
  
  form = LocationForm(initial={'name': district.name})
  return render(request, 'management/locations/districts.html', {
    'nav_link': nav_link,
    'department': department,
    'province': province,
    'district': district,
    'editing': True,
    'form': form
  })

def districts_delete(request, department_id, province_id, district_id):
  success, error = LocationService.delete_location(district_id)
  if error:
    messages.error(request, f'Error: {error}')
  else:
    messages.success(request, 'Distrito eliminado')
  return redirect('locations_districts', department_id=department_id, province_id=province_id)