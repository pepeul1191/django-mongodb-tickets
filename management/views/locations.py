from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from management.models import Location 
from mongoengine.errors import DoesNotExist
from management.forms.locations_forms import DepartmentForm

nav_link = 'locations'

def locations(request):
  if request.method == 'GET':
    departments = Location.objects.filter(type="department")

    context = {
      'page_title': 'Gestión de Locaciones',
      'nav_link': 'locations',
      'departments': departments,
      'provinces': None,
      'districts': None,
    }

    return render(request, 'management/locations/index.html', context)
  else:
    return JsonResponse({
        'status': 'form_error',
        'errors': 'XD'
    }, status=400)

def locations_provinces(request, department_id):
  try:
    departments = Location.objects.filter(type="department")

    department = Location.objects.get(id=ObjectId(department_id))

    provinces = Location.objects.filter(type="province", parent_id=department.id)

    context = {
      'nav_link': 'locations',
      'departments': departments,
      'department': department,
      'provinces': provinces,
      'districts': None,
      'page_title': f'Provincias de {department.name}'
    }
    return render(request, 'management/locations/index.html', context)
  except (DoesNotExist, Exception) as e:
    # Manejar error si el ID no existe o es inválido
    return render(request, '404.html', status=404)
  
def locations_districts(request, department_id, province_id):
  try:
    departments = Location.objects.filter(type="department")

    department = Location.objects.get(id=ObjectId(department_id))

    provinces = Location.objects.filter(type="province", parent_id=department.id)

    province = Location.objects.get(id=ObjectId(province_id))

    districts = Location.objects.filter(type="district", parent_id=province.id)

    context = {
      'nav_link': nav_link,
      'departments': departments,
      'department': department,
      'provinces': provinces,
      'province': province,
      'districts': districts,
      'page_title': f'Provincias de {department.name}'
    }
    return render(request, 'management/locations/index.html', context)
  except (DoesNotExist, Exception) as e:
    # Manejar error si el ID no existe o es inválido
    return render(request, '404.html', status=404)
  
def departments(request):
  context = {
    'nav_link': nav_link,
  }

  if request.method == 'POST':
    form = DepartmentForm(request.POST)
    
    if form.is_valid():
      try:
        department = Location(
          name=form.cleaned_data['name'],
          type='department',
          parent_id=None,
        )
        department.save()
        messages.success(request, 'Departamento agregado exitosamente.')
        return redirect('locations')

      except Exception as e:
        messages.error(request, f'Error en MongoDB: {str(e)}')
        return render(request, 'management/locations/departments.html', context)
    else:
      context['form'] = form
      messages.error(request, 'Formulario no válido, no se pudo grabar el departamento.')
      return render(request, 'management/locations/departments.html', context, status=401)
  elif request.method == 'GET':
    return render(request, 'management/locations/departments.html', context)

def departments_edit(request, department_id):
  context = {
    'nav_link': nav_link,
    'editing': True,
  }

  if request.method == 'POST':
    form = DepartmentForm(request.POST)
    
    if form.is_valid():
      try:
        department = Location.objects.get(id=ObjectId(department_id))
        # Actualizar el departamento existente
        department.name = form.cleaned_data['name']
        department.save()  # Esto actualizará el documento existente
        
        messages.success(request, 'Departamento actualizado exitosamente.')
        return redirect('locations')

      except Exception as e:
        messages.error(request, f'Error en MongoDB: {str(e)}')
        return render(request, 'management/locations/departments.html', context)
    else:
      context['form'] = form
      messages.error(request, 'Formulario no válido, no se pudo actualizar el departamento.')
      return render(request, 'management/locations/departments.html', context, status=401)
      
  elif request.method == 'GET':
    try:
      department = Location.objects.get(id=ObjectId(department_id))
      context['editing'] = True
      form = DepartmentForm(initial={
        'id': department.id,
        'name': department.name,
        'parent_id': department.parent_id,
      })
      
      context['form'] = form
      return render(request, 'management/locations/departments.html', context)
    except (DoesNotExist, Exception) as e:
      # Manejar error si el ID no existe o es inválido
      return render(request, '404.html', status=404)

def departments_delete(request, department_id):
  context = {
    'nav_link': nav_link,
  }

  try:
    department = Location.objects.get(id=ObjectId(department_id))
    department.delete()
    
    messages.success(request, 'Departamento eliminado exitosamente.')
    return redirect('locations')
  except (DoesNotExist, Exception) as e:
    # Manejar error si el ID no existe o es inválido
    return render(request, '404.html', status=404)

def provinces_edit(request, department_id, province_id):
  pass

def provinces_delete(request, department_id, province_id):
  pass

def provinces_add(request, department_id):
  context = {
    'nav_link': nav_link,
  }

  if request.method == 'POST':
    form = DepartmentForm(request.POST)
    
    if form.is_valid():
      try:
        department = Location(
          name=form.cleaned_data['name'],
          type='department',
          parent_id=None,
        )
        department.save()
        messages.success(request, 'Departamento agregado exitosamente.')
        return redirect('locations')

      except Exception as e:
        messages.error(request, f'Error en MongoDB: {str(e)}')
        return render(request, 'management/locations/provinces.html', context)
    else:
      context['form'] = form
      messages.error(request, 'Formulario no válido, no se pudo grabar el departamento.')
      return render(request, 'management/locations/provinces.html', context, status=401)
  elif request.method == 'GET':
    try:
      department = Location.objects.get(id=ObjectId(department_id))
      context['department'] = department
      return render(request, 'management/locations/provinces.html', context)
    except Exception as e:
      messages.error(request, f'Error en MongoDB: {str(e)}')
      return redirect(f"/management/locations/")

def districts(request):
  pass