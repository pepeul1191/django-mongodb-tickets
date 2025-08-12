from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.enterprise_forms import EnterpriseForm
from mongoengine.errors import DoesNotExist
from management.models.enterprise import Enterprise
from datetime import datetime
import math

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


def enterprises_add(request):
  context = {
    'page_title': 'Gestión de Empresas',
    'nav_link': 'enlace_de_navegacion', # Reemplaza con la variable correcta
    'editing': False, # Indica que es un formulario para crear, no para editar
  }

  if request.method == 'GET':
    form = EnterpriseForm()
    context['form'] = form
    return render(request, 'management/enterprises/detail.html', context)
  
  elif request.method == 'POST':
    form = EnterpriseForm(request.POST)
    
    if form.is_valid():
      try:
        # Crea una nueva instancia de Enterprise a partir de los datos validados
        enterprise = Enterprise(
          business_name=form.cleaned_data['business_name'],
          trade_name=form.cleaned_data['trade_name'],
          tax_id=form.cleaned_data['tax_id'],
          fiscal_address=form.cleaned_data['fiscal_address'],
          location_id=ObjectId(form.cleaned_data['location_id']),
          phone=form.cleaned_data['phone'],
          email=form.cleaned_data['email'],
          website=form.cleaned_data['website'],
          image_url=request.POST.get('image_url', '')
        )
        
        # Guarda el objeto en la base de datos
        enterprise.save()

        messages.success(request, '¡Empresa creada exitosamente!')
        # Redirige a la página de detalle de la nueva empresa
        return redirect('enterprise_detail', enterprise_id=str(enterprise.id))
      
      except Exception as e:
        messages.error(request, f'Error al crear la empresa en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/enterprises/detail.html', context, status=500)
    else:
      # Si el formulario no es válido, muestra los errores específicos
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/enterprises/detail.html', context, status=400)
  
  else:
    # Manejar otros métodos de solicitud no permitidos
    return JsonResponse({
      'status': 'error',
      'message': 'Método no permitido.'
    }, status=405)

def create_enterprise(request):
  context = {}
  
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
  context = {
    'editing': True,
  }
  
  try:
    # Use get_object_or_404 for cleaner error handling
    enterprise = get_object_or_404(Enterprise, pk=ObjectId(enterprise_id))
  except Exception as e:
    messages.error(request, f'Error al buscar la empresa: {str(e)}')
    return redirect('enterprises_list')

  if request.method == 'POST':
    # Instantiate the form with POST data and the existing instance
    form = EnterpriseForm(request.POST, instance=enterprise)
    
    if form.is_valid():
      try:
        # Save the form data to the existing enterprise object
        form.save()
        
        # Handle the image_url field separately if needed
        # Your form logic might handle this better, but this matches your original code
        if 'image_url' in request.POST and request.POST['image_url']:
          enterprise.image_url = request.POST['image_url']
        else:
          # Consider not overwriting if no new image is provided
          pass 

        enterprise.save() # Save again to persist image_url change
        
        messages.success(request, 'Empresa actualizada exitosamente.')
        # Redirect to the detail page for the updated enterprise
        return redirect('enterprise_detail', enterprise_id=str(enterprise.id))
      
      except Exception as e:
        messages.error(request, f'Error al actualizar en MongoDB: {str(e)}')
        context['form'] = form
        context['enterprise'] = enterprise
        return render(request, 'management/enterprises/detail.html', context, status=500)
    else:
      # If the form is not valid, re-render the page with errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      context['enterprise'] = enterprise
      return render(request, 'management/enterprises/detail.html', context, status=400)
  
  # If it's a GET request, populate the form with the existing enterprise data
  else:
    # Use `instance=enterprise` to automatically populate the form fields
    form = EnterpriseForm(instance=enterprise)
    context['form'] = form
    context['enterprise'] = enterprise
    return render(request, 'management/enterprises/detail.html', context)