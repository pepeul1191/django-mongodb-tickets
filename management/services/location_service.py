from bson import ObjectId
from mongoengine.errors import DoesNotExist
from management.models.location import Location

class LocationService:
  
  @staticmethod
  def get_departments():
    return Location.objects.filter(type="department")
  
  @staticmethod
  def get_location_by_id(location_id):
    try:
      return Location.objects.get(id=ObjectId(location_id))
    except (DoesNotExist, Exception):
      return None
  
  @staticmethod
  def get_provinces_by_department(department_id):
    department = LocationService.get_location_by_id(department_id)
    if department:
      return Location.objects.filter(type="province", parent_id=department.id)
    return []
  
  @staticmethod
  def get_districts_by_province(province_id):
    province = LocationService.get_location_by_id(province_id)
    if province:
      return Location.objects.filter(type="district", parent_id=province.id)
    return []
  
  @staticmethod
  def create_location(name, location_type, parent_id=None):
    try:
      location = Location(
        name=name,
        type=location_type,
        parent_id=parent_id
      )
      location.save()
      return location, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_location(location_id, name):
    try:
      location = LocationService.get_location_by_id(location_id)
      if location:
        location.name = name
        location.save()
        return location, None
      return None, "Ubicación no encontrada"
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_location(location_id):
    try:
      location = LocationService.get_location_by_id(location_id)
      if location:
        location.delete()
        return True, None
      return False, "Ubicación no encontrada"
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def validate_parent_child_relationship(parent_id, child_type):
    if not parent_id:
      return True, None
    
    parent = LocationService.get_location_by_id(parent_id)
    if not parent:
      return False, "Parent no encontrado"
    
    valid_relationships = {
      'department': 'province',
      'province': 'district'
    }
    
    if parent.type in valid_relationships and valid_relationships[parent.type] == child_type:
      return True, None
    
    return False, f"Relación inválida: {parent.type} no puede tener hijos de tipo {child_type}"