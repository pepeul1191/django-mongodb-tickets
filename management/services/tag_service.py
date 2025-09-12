# management/services/tag_service.py
from datetime import datetime
from bson import ObjectId
from mongoengine.queryset import Q
from management.models.tag import Tag
import math

class TagService:
  
  @staticmethod
  def get_tags_list(page_number=1, per_page=10, search_query=''):
    """Obtener lista paginada de tags con filtros"""
    try:
      page_number = int(page_number)
      per_page = int(per_page)
    except (ValueError, TypeError):
      page_number = 1
      per_page = 10
    
    if page_number < 1:
      page_number = 1
    if per_page < 1:
      per_page = 10

    tags = Tag.objects.all()
    
    if search_query:
      tags = tags.filter(Q(name__icontains=search_query))

    total_tags = tags.count()
    total_pages = math.ceil(total_tags / per_page)
    
    offset = (page_number - 1) * per_page
    paginated_tags = tags.skip(offset).limit(per_page)

    return {
      'tags': paginated_tags,
      'total_tags': total_tags,
      'total_pages': total_pages,
      'page_number': page_number,
      'per_page': per_page,
      'offset': offset
    }
  
  @staticmethod
  def get_tag_by_id(tag_id):
    """Obtener tag por ID"""
    try:
      return Tag.objects.get(id=ObjectId(tag_id))
    except Tag.DoesNotExist:
      return None
    except Exception:
      return None
  
  @staticmethod
  def create_tag(name):
    """Crear nuevo tag"""
    try:
      tag = Tag(name=name)
      tag.save()
      return tag, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_tag(tag_id, name):
    """Actualizar tag existente"""
    try:
      tag = TagService.get_tag_by_id(tag_id)
      if not tag:
        return None, "Tag no encontrado"
      
      tag.name = name
      tag.updated = datetime.utcnow()
      tag.save()
      
      return tag, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_tag(tag_id):
    """Eliminar tag"""
    try:
      tag = TagService.get_tag_by_id(tag_id)
      if not tag:
        return False, "Tag no encontrado"
      
      tag_name = tag.name
      tag.delete()
      return True, tag_name
    except Exception as e:
      return False, str(e)