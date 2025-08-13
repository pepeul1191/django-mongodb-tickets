from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.assets_forms import AssetForm
from management.forms.documents_forms import AssetDocumentForm
from mongoengine.errors import DoesNotExist
from management.models.asset import Asset
from datetime import datetime
import math

from management.models.document_embedded import DocumentEmbedded
from management.models.location import Location

nav_link = 'assets'

def assets_list(request):
  # Obtener parámetros de la URL
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  code_query = request.GET.get('code', '') 

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

  # Consultar y filtrar las activos
  assets = Asset.objects.all()
  # Construir una lista de consultas Q para combinar
  query_list = []
  if search_query:
    query_list.append(Q(name__icontains=search_query) | Q(description__icontains=search_query))

  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    assets = assets.filter(combined_query)

  if code_query:
    query_list.append(Q(code__icontains=code_query))

  # Aplicar filtros si hay consultas
  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    assets = assets.filter(combined_query)

  # Lógica de paginación
  total_assets = assets.count()
  total_pages = math.ceil(total_assets / per_page)
  
  # Calcular el offset para la consulta (skip)
  offset = (page_number - 1) * per_page
  
  # Obtener las empresas para la página actual
  paginated_assets = assets.skip(offset).limit(per_page)

  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Activos',
    'assets': paginated_assets,
    'search_query': search_query,
    'code_query': code_query,
    'page': page_number,
    'per_page': per_page,
    'total_assets': total_assets,
    'total_pages': total_pages,
    'start_record': offset + 1,
    'end_record': min(offset + per_page, total_assets),
  }

  return render(request, 'management/assets/list.html', context)

def delete_asset(request, asset_id):
  if request.method == 'GET':
    try:
      # Usamos el ObjectId para encontrar el documento
      asset = Asset.objects.get(id=ObjectId(asset_id))
      asset.delete()
      messages.success(request, f'El activo "{asset.name}" ha sido eliminada correctamente.')
    except Asset.DoesNotExist:
      messages.error(request, 'El activo no fue encontrada.')
    except Exception as e:
      messages.error(request, f'Ocurrió un error al intentar eliminar el activo: {e}')
    
    return redirect('assets_list')
  else:
    # Si la solicitud no es POST, puedes redirigir o mostrar una página de confirmación
    # Para este ejemplo, simplemente redirigimos de vuelta a la lista
    return redirect('assets_list')

def create_asset(request):
  context = {
    "nav_link": nav_link
  }
  
  if request.method == 'POST':
    form = AssetForm(request.POST)
    
    if form.is_valid():
      try:
        # Create a new asset with form data
        asset = Asset(
          name=form.cleaned_data['name'],
          description=form.cleaned_data['description'],
          code=form.cleaned_data['code'],
          documents=[],
        )
        
        # Save to MongoDB
        asset.save()

        # Success message and redirect
        messages.success(request, '¡Activo creado exitosamente!')
        return redirect('asset_detail', asset_id=str(asset.id))
          
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/assets/detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/assets/detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = AssetForm()
  return render(request, 'management/assets/detail.html', context)

def update_asset(request, asset_id):
  """
  Vista para editar una empresa existente usando un forms.Form.
  Maneja la carga del formulario con datos iniciales (GET) y
  el guardado manual de los datos (POST).
  """
  try:
    # 1. Obtener la instancia de la empresa de la base de datos
    asset = Asset.objects.get(id=ObjectId(asset_id))
  except Asset.DoesNotExist:
    messages.error(request, 'La empresa no fue encontrada.')
    return redirect('assets_list')
  except Exception as e:
    messages.error(request, f'Error al buscar la empresa: {e}')
    return redirect('assets_list')

  if request.method == 'POST':
    # 2. Para POST, inicializar el formulario con los datos enviados
    form = AssetForm(request.POST)
    if form.is_valid():
      # 3. Acceder a los datos limpios y actualizar el objeto manualmente
      cleaned_data = form.cleaned_data
      
      # Mapear los campos del formulario a los del modelo
      asset.name = cleaned_data['name']
      asset.description = cleaned_data['description']
      asset.code = cleaned_data['code']
      
      # 4. Guardar los cambios en la base de datos
      asset.save() 
      
      messages.success(request, f'El activo "{asset.name}" ha sido actualizada correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    # 5. Para GET, crear un diccionario con los datos del objeto
    #    y pasar el diccionario al parámetro 'initial'
    initial_data = {
      'id': str(asset.id),
      'name': asset.name,
      'description': asset.description,
      'code': asset.code,
    }
    form = AssetForm(initial=initial_data)
  context = {
    'editing': True,
    'form': form,
    'asset': asset,
    'page_title': 'Editar Activo',
    'nav_link': nav_link, 
  }
  return render(request, 'management/assets/detail.html', context)

def asset_add_document(request, asset_id):
  context = {
    "nav_link": nav_link,
    "asset_id": asset_id
  }

  if request.method == 'POST':
    form = AssetDocumentForm(request.POST)
    
    if form.is_valid():
      try:
        
        # 1. Obtener la instancia de la empresa de la base de datos
        asset = Asset.objects.get(id=ObjectId(asset_id))

        # Create a new enterprise with form data
        document = DocumentEmbedded(
          name=form.cleaned_data['name'],
          size=form.cleaned_data['size'],
          mime=form.cleaned_data['mime'],
          url=request.POST.get('image_url', '')  # File upload field
        )

        asset.documents.append(document)
        asset.save()

        # Success message and redirect
        messages.success(request, 'Documento agregado exitosamente!')
        return redirect('update_asset', asset_id=asset_id)
      except Asset.DoesNotExist:
        messages.error(request, 'La empresa no fue encontrada.')
        return redirect('assets_list')  
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/assets/documents_detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/assets/documents_detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = AssetDocumentForm()
  return render(request, 'management/assets/documents_detail.html', context)

def asset_delete_document(request, asset_id, document_id):
  pass