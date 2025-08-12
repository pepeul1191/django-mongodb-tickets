from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.enterprises_forms import EnterpriseForm
from mongoengine.errors import DoesNotExist
from management.models.enterprise import Enterprise
from datetime import datetime
import math

from management.models.location import Location

nav_link = 'enterprises'

def enterprises_list(request):
  # Obtener parámetros de la URL
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  tax_id_query = request.GET.get('tax_id', '') 

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
  enterprises = Enterprise.objects.all()
  # Construir una lista de consultas Q para combinar
  query_list = []
  if search_query:
    query_list.append(Q(business_name__icontains=search_query) | Q(trade_name__icontains=search_query))
  
  if tax_id_query:
    query_list.append(Q(tax_id__icontains=tax_id_query))

  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    enterprises = enterprises.filter(combined_query)

  # Lógica de paginación
  total_enterprises = enterprises.count()
  total_pages = math.ceil(total_enterprises / per_page)
  
  # Calcular el offset para la consulta (skip)
  offset = (page_number - 1) * per_page
  
  # Obtener las empresas para la página actual
  paginated_enterprises = enterprises.skip(offset).limit(per_page)

  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Empresas',
    'enterprises': paginated_enterprises,
    'search_query': search_query,
    'page': page_number,
    'per_page': per_page,
    'tax_id_query': tax_id_query,
    'total_enterprises': total_enterprises,
    'total_pages': total_pages,
    'start_record': offset + 1,
    'end_record': min(offset + per_page, total_enterprises),
  }

  return render(request, 'management/enterprises/list.html', context)

def delete_enterprise(request, enterprise_id):
  if request.method == 'GET':
    try:
      # Usamos el ObjectId para encontrar el documento
      enterprise = Enterprise.objects.get(id=ObjectId(enterprise_id))
      enterprise.delete()
      messages.success(request, f'La empresa "{enterprise.business_name}" ha sido eliminada correctamente.')
    except Enterprise.DoesNotExist:
      messages.error(request, 'La empresa no fue encontrada.')
    except Exception as e:
      messages.error(request, f'Ocurrió un error al intentar eliminar la empresa: {e}')
    
    return redirect('enterprises_list')
  else:
    # Si la solicitud no es POST, puedes redirigir o mostrar una página de confirmación
    # Para este ejemplo, simplemente redirigimos de vuelta a la lista
    return redirect('enterprises_list')

def create_enterprise(request):
  context = {
    "nav_link": nav_link
  }
  
  if request.method == 'POST':
    form = EnterpriseForm(request.POST)
    
    if form.is_valid():
      try:
        # Create a new enterprise with form data
        enterprise = Enterprise(
          business_name=form.cleaned_data['business_name'],
          trade_name=form.cleaned_data['trade_name'],
          tax_id=form.cleaned_data['tax_id'],
          fiscal_address=form.cleaned_data['fiscal_address'],
          location_id=ObjectId(form.cleaned_data['location_id']),
          phone=form.cleaned_data['phone'],
          email=form.cleaned_data['email'],
          website=form.cleaned_data['website'],
          image_url=request.POST.get('image_url', '')  # File upload field
        )
        
        # Save to MongoDB
        enterprise.save()

        # Success message and redirect
        messages.success(request, '¡Empresa creada exitosamente!')
        return redirect('enterprise_detail', enterprise_id=str(enterprise.id))
          
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/enterprises/detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/enterprises/detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = EnterpriseForm()
  return render(request, 'management/enterprises/detail.html', context)

def update_enterprise(request, enterprise_id):
  """
  Vista para editar una empresa existente usando un forms.Form.
  Maneja la carga del formulario con datos iniciales (GET) y
  el guardado manual de los datos (POST).
  """
  try:
    # 1. Obtener la instancia de la empresa de la base de datos
    enterprise = Enterprise.objects.get(id=ObjectId(enterprise_id))
    location_data = Location.get_district_with_hierarchy(enterprise.location_id)
  except Enterprise.DoesNotExist:
    messages.error(request, 'La empresa no fue encontrada.')
    return redirect('enterprises_list')
  except Exception as e:
    messages.error(request, f'Error al buscar la empresa: {e}')
    return redirect('enterprises_list')

  if request.method == 'POST':
    # 2. Para POST, inicializar el formulario con los datos enviados
    form = EnterpriseForm(request.POST)
    if form.is_valid():
      # 3. Acceder a los datos limpios y actualizar el objeto manualmente
      cleaned_data = form.cleaned_data
      
      # Mapear los campos del formulario a los del modelo
      enterprise.business_name = cleaned_data['business_name']
      enterprise.trade_name = cleaned_data['trade_name']
      enterprise.tax_id = cleaned_data['tax_id']
      enterprise.phone = cleaned_data['phone']
      enterprise.website = cleaned_data['website']
      enterprise.email = cleaned_data['email']
      enterprise.location_id = ObjectId(cleaned_data['location_id'])
      enterprise.fiscal_address = cleaned_data['fiscal_address']
      enterprise.image_url = cleaned_data['image_url']
      
      # 4. Guardar los cambios en la base de datos
      enterprise.save() 
      
      messages.success(request, f'La empresa "{enterprise.business_name}" ha sido actualizada correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    # 5. Para GET, crear un diccionario con los datos del objeto
    #    y pasar el diccionario al parámetro 'initial'
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