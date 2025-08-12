from datetime import datetime
from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mongoengine.queryset import Q # Usa esta importación
from management.forms.tags_forms import TagForm
from management.models.tag import Tag
import math

nav_link = 'tags'

def tags_list(request):
  # Obtener parámetros de la URL
  page_number = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)
  search_query = request.GET.get('name', '')

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

  # Consultar y filtrar El etiquetas
  tags = Tag.objects.all()
  # Construir una lista de consultas Q para combinar
  query_list = []
  if search_query:
    query_list.append(Q(name__icontains=search_query))
  

  if query_list:
    # Combinar todas las consultas con AND
    combined_query = query_list[0]
    for q in query_list[1:]:
      combined_query &= q
    tags = tags.filter(combined_query)

  # Lógica de paginación
  total_tags = tags.count()
  total_pages = math.ceil(total_tags / per_page)
  
  # Calcular el offset para la consulta (skip)
  offset = (page_number - 1) * per_page
  
  # Obtener El etiquetas para la página actual
  paginated_tags = tags.skip(offset).limit(per_page)

  context = {
    'nav_link': nav_link,
    'page_title': 'Gestión de Etiquetas',
    'tags': paginated_tags,
    'search_query': search_query,
    'page': page_number,
    'per_page': per_page,
    'total_tags': total_tags,
    'total_pages': total_pages,
    'start_record': offset + 1,
    'end_record': min(offset + per_page, total_tags),
  }

  return render(request, 'management/tags/list.html', context)

def delete_tag(request, tag_id):
  if request.method == 'GET':
    try:
      # Usamos el ObjectId para encontrar el documento
      tag = Tag.objects.get(id=ObjectId(tag_id))
      tag.delete()
      messages.success(request, f'El etiqueta "{Tag.name}" ha sido eliminada correctamente.')
    except tag.DoesNotExist:
      messages.error(request, 'El etiqueta no fue encontrada.')
    except Exception as e:
      messages.error(request, f'Ocurrió un error al intentar eliminar el etiqueta: {e}')
    
    return redirect('tags_list')
  else:
    # Si la solicitud no es POST, puedes redirigir o mostrar una página de confirmación
    # Para este ejemplo, simplemente redirigimos de vuelta a la lista
    return redirect('tags_list')

def create_tag(request):
  context = {
    "nav_link": nav_link
  }
  
  if request.method == 'POST':
    form = TagForm(request.POST)
    
    if form.is_valid():
      try:
        # Create a new tag with form data
        tag = Tag(
          name=form.cleaned_data['name'],
        )
        
        # Save to MongoDB
        tag.save()

        # Success message and redirect
        messages.success(request,'¡etiqueta creado exitosamente!')
        return redirect('tag_detail', tag_id=str(tag.id))
          
      except Exception as e:
        messages.error(request, f'Error al crear en MongoDB: {str(e)}')
        context['form'] = form
        return render(request, 'management/tags/detail.html', context, status=500)
    else:
      # Show specific form errors
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{form.fields[field].label}: {error}")
      
      context['form'] = form
      return render(request, 'management/tags/detail.html', context, status=400)
  
  # If it's a GET request, show an empty form
  context['form'] = TagForm()
  return render(request, 'management/tags/detail.html', context)

def update_tag(request, tag_id):
  """
  Vista para editar El tag existente usando un forms.Form.
  Maneja la carga del formulario con datos iniciales (GET) y
  el guardado manual de los datos (POST).
  """
  try:
    # 1. Obtener la instancia de El etiqueta de la base de datos
    tag = Tag.objects.get(id=ObjectId(tag_id))
  except Tag.DoesNotExist:
    messages.error(request, 'El etiqueta no fue encontrada.')
    return redirect('tags_list')
  except Exception as e:
    messages.error(request, f'Error al buscar la etiqueta: {e}')
    return redirect('tags_list')

  if request.method == 'POST':
    # 2. Para POST, inicializar el formulario con los datos enviados
    form = TagForm(request.POST)
    if form.is_valid():
      # 3. Acceder a los datos limpios y actualizar el objeto manualmente
      cleaned_data = form.cleaned_data
      
      # Mapear los campos del formulario a los del modelo
      tag.name = cleaned_data['name']
      tag.updated = datetime.utcnow()
      
      # 4. Guardar los cambios en la base de datos
      tag.save() 
      
      messages.success(request, f'El etiqueta "{tag.name}" ha sido actualizadaoc orrectamente.')
    else:
      messages.error(request, 'Por favor, corrige los errores en el formulario.')
  else:
    # 5. Para GET, crear un diccionario con los datos del objeto
    #    y pasar el diccionario al parámetro 'initial'
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