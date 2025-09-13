# management/services/role_service.py
from bson import ObjectId
from mongoengine.queryset import Q
from mongoengine.errors import DoesNotExist
from datetime import datetime
import math
from management.models.role import Role

class RoleService:
  
  @staticmethod
  def get_roles_list(page_number=1, per_page=10, search_query=''):
    """Obtener lista paginada de roles con filtros"""
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

    roles = Role.objects.all()
    
    if search_query:
      roles = roles.filter(Q(name__icontains=search_query))

    total_roles = roles.count()
    total_pages = math.ceil(total_roles / per_page)
    
    offset = (page_number - 1) * per_page
    paginated_roles = roles.skip(offset).limit(per_page)

    return {
      'roles': paginated_roles,
      'total_roles': total_roles,
      'total_pages': total_pages,
      'page_number': page_number,
      'per_page': per_page,
      'offset': offset
    }
  
  @staticmethod
  def get_role_by_id(role_id):
    """Obtener rol por ID"""
    try:
      return Role.objects.get(id=ObjectId(role_id))
    except Role.DoesNotExist:
      return None
    except Exception:
      return None
  
  @staticmethod
  def create_role(name, description):
    """Crear nuevo rol"""
    try:
      role = Role(name=name, description=description)
      role.save()
      return role, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_role(role_id, name, description):
    """Actualizar rol existente"""
    try:
      role = RoleService.get_role_by_id(role_id)
      if not role:
        return None, "Rol no encontrado"
      
      role.name = name
      role.description = description
      role.save()
      
      return role, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_role(role_id):
    """Eliminar rol"""
    try:
      role = RoleService.get_role_by_id(role_id)
      if not role:
        return False, "Rol no encontrado"
      
      role_name = role.name
      role.delete()
      return True, role_name
    except Exception as e:
      return False, str(e)