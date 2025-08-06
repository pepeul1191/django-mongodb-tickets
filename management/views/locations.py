from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render
from management.models import Location 
from mongoengine.errors import DoesNotExist

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
      'nav_link': 'locations',
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
  
