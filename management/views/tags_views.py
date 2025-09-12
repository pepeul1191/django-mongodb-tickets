# management/views/tags_view.py
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from management.services.tag_service import TagService
from management.forms.tags_forms import TagForm

nav_link = 'tags'

def tags_list(request):
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')

  result = TagService.get_tags_list(page_number, per_page, search_query)
  
  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Etiquetas',
    'tags': result['tags'],
    'search_query': search_query,
    'page': result['page_number'],
    'per_page': result['per_page'],
    'total_tags': result['total_tags'],
    'total_pages': result['total_pages'],
    'start_record': result['offset'] + 1,
    'end_record': min(result['offset'] + result['per_page'], result['total_tags']),
  }

  return render(request, 'management/tags/list.html', context)

def delete_tag(request, tag_id):
  if request.method == 'GET':
    success, result = TagService.delete_tag(tag_id)
    
    if success:
      messages.success(request, f'El etiqueta "{result}" ha sido eliminada correctamente.')
    else:
      messages.error(request, f'Ocurrió un error al intentar eliminar el etiqueta: {result}')
    
    return redirect('tags_list')
  else:
    return redirect('tags_list')

def create_tag(request):
  context = {
    "nav_link": nav_link
  }
  
  if request.method == 'POST':
    form = TagForm(request.POST)
    
    if form.is_valid():
      tag, error = TagService.create_tag(form.cleaned_data['name'])
      
      if error:
        messages.error(request, f'Error al crear en MongoDB: {error}')
        context['form'] = form
        return render(request, 'management/tags/detail.html', context, status=500)
      else:
        messages.success(request, '¡Etiqueta creada exitosamente!')
        return redirect('tag_detail', tag_id=str(tag.id))
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/tags/detail.html', context, status=400)
  
  context['form'] = TagForm()
  return render(request, 'management/tags/detail.html', context)

def update_tag(request, tag_id):
  tag = TagService.get_tag_by_id(tag_id)
  
  if not tag:
    messages.error(request, 'El etiqueta no fue encontrada.')
    return redirect('tags_list')

  if request.method == 'POST':
    form = TagForm(request.POST)
    
    if form.is_valid():
      updated_tag, error = TagService.update_tag(tag_id, form.cleaned_data['name'])
      
      if error:
        messages.error(request, f'Error al actualizar: {error}')
      else:
        messages.success(request, f'El etiqueta "{updated_tag.name}" ha sido actualizada correctamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    initial_data = {
      'id': str(tag.id),
      'name': tag.name,
    }
    form = TagForm(initial=initial_data)
  
  context = {
    'editing': True,
    'form': form,
    'tag': tag,
    'page_title': 'Editar etiqueta',
    'nav_link': nav_link, 
  }
  
  return render(request, 'management/tags/detail.html', context)