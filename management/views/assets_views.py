# management/views/assets_views.py
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from management.services.asset_service import AssetService
from management.forms.assets_forms import AssetForm
from management.forms.documents_forms import AssetDocumentForm

nav_link = 'assets'

def assets_list(request):
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')
  code_query = request.GET.get('code', '')

  result = AssetService.get_assets_list(page_number, per_page, search_query, code_query)
  
  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Activos',
    'assets': result['assets'],
    'search_query': search_query,
    'code_query': code_query,
    'page': result['page_number'],
    'per_page': result['per_page'],
    'total_assets': result['total_assets'],
    'total_pages': result['total_pages'],
    'start_record': result['offset'] + 1,
    'end_record': min(result['offset'] + result['per_page'], result['total_assets']),
  }

  return render(request, 'management/assets/list.html', context)

def delete_asset(request, asset_id):
  if request.method == 'GET':
    success, result = AssetService.delete_asset(asset_id)
    
    if success:
      messages.success(request, f'El activo "{result}" ha sido eliminado correctamente.')
    else:
      messages.error(request, f'Ocurrió un error al intentar eliminar el activo: {result}')
    
    return redirect('assets_list')
  else:
    return redirect('assets_list')

def create_asset(request):
  context = {"nav_link": nav_link}
  
  if request.method == 'POST':
    form = AssetForm(request.POST)
    
    if form.is_valid():
      asset, error = AssetService.create_asset(
        form.cleaned_data['name'],
        form.cleaned_data['description'],
        form.cleaned_data['code']
      )
      
      if error:
        messages.error(request, f'Error al crear en MongoDB: {error}')
        context['form'] = form
        return render(request, 'management/assets/detail.html', context, status=500)
      else:
        messages.success(request, '¡Activo creado exitosamente!')
        return redirect('asset_detail', asset_id=str(asset.id))
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/assets/detail.html', context, status=400)
  
  context['form'] = AssetForm()
  return render(request, 'management/assets/detail.html', context)

def update_asset(request, asset_id):
  asset = AssetService.get_asset_by_id(asset_id)
  
  if not asset:
    messages.error(request, 'El activo no fue encontrado.')
    return redirect('assets_list')

  if request.method == 'POST':
    form = AssetForm(request.POST)
    
    if form.is_valid():
      updated_asset, error = AssetService.update_asset(
        asset_id,
        form.cleaned_data['name'],
        form.cleaned_data['description'],
        form.cleaned_data['code']
      )
      
      if error:
        messages.error(request, f'Error al actualizar: {error}')
      else:
        messages.success(request, f'El activo "{updated_asset.name}" ha sido actualizado correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
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
      asset, error = AssetService.add_document_to_asset(
        asset_id,
        form.cleaned_data['name'],
        form.cleaned_data['size'],
        form.cleaned_data['mime'],
        request.POST.get('image_url', '')
      )
      
      if error:
        messages.error(request, f'Error al agregar documento: {error}')
        context['form'] = form
        return render(request, 'management/assets/documents_detail.html', context, status=500)
      else:
        messages.success(request, 'Documento agregado exitosamente!')
        return redirect('update_asset', asset_id=asset_id)
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/assets/documents_detail.html', context, status=400)
  
  context['form'] = AssetDocumentForm()
  return render(request, 'management/assets/documents_detail.html', context)

def asset_delete_document(request, asset_id, document_id):
  success, error = AssetService.delete_document_from_asset(asset_id, document_id)
  
  if error:
    messages.error(request, f"Error al eliminar documento: {error}")
  else:
    messages.success(request, "Documento eliminado correctamente")
  
  return redirect('update_asset', asset_id=asset_id)