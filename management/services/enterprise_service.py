# management/services/enterprise_service.py
import json
from bson import ObjectId
from mongoengine.queryset import Q
from mongoengine.errors import DoesNotExist
from datetime import datetime
import math
from management.models.enterprise import Enterprise
from management.models.asset import Asset
from management.models.employee import Employee
from management.models.location import Location

class EnterpriseService:
  
  @staticmethod
  def get_enterprises_list(page_number=1, per_page=10, search_query='', tax_id_query=''):
    """Obtener lista paginada de empresas con filtros"""
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

    enterprises = Enterprise.objects.all()
    
    query_list = []
    if search_query:
      query_list.append(Q(business_name__icontains=search_query) | Q(trade_name__icontains=search_query))
    if tax_id_query:
      query_list.append(Q(tax_id__icontains=tax_id_query))

    if query_list:
      combined_query = query_list[0]
      for q in query_list[1:]:
        combined_query &= q
      enterprises = enterprises.filter(combined_query)

    total_enterprises = enterprises.count()
    total_pages = math.ceil(total_enterprises / per_page)
    
    offset = (page_number - 1) * per_page
    paginated_enterprises = enterprises.skip(offset).limit(per_page)

    return {
      'enterprises': paginated_enterprises,
      'total_enterprises': total_enterprises,
      'total_pages': total_pages,
      'page_number': page_number,
      'per_page': per_page,
      'offset': offset
    }
  
  @staticmethod
  def get_enterprise_by_id(enterprise_id):
    """Obtener empresa por ID"""
    try:
      return Enterprise.objects.get(id=ObjectId(enterprise_id))
    except Enterprise.DoesNotExist:
      return None
    except Exception:
      return None
  
  @staticmethod
  def create_enterprise(business_name, trade_name, tax_id, fiscal_address, 
                       location_id, phone, email, website, image_url=''):
    """Crear nueva empresa"""
    try:
      enterprise = Enterprise(
        business_name=business_name,
        trade_name=trade_name,
        tax_id=tax_id,
        fiscal_address=fiscal_address,
        location_id=ObjectId(location_id),
        phone=phone,
        email=email,
        website=website,
        image_url=image_url
      )
      enterprise.save()
      return enterprise, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_enterprise(enterprise_id, business_name, trade_name, tax_id, 
                       fiscal_address, location_id, phone, email, website, image_url):
    """Actualizar empresa existente"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      if not enterprise:
        return None, "Empresa no encontrada"
      
      enterprise.business_name = business_name
      enterprise.trade_name = trade_name
      enterprise.tax_id = tax_id
      enterprise.fiscal_address = fiscal_address
      enterprise.location_id = ObjectId(location_id)
      enterprise.phone = phone
      enterprise.email = email
      enterprise.website = website
      enterprise.image_url = image_url
      enterprise.save()
      
      return enterprise, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_enterprise(enterprise_id):
    """Eliminar empresa"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      if not enterprise:
        return False, "Empresa no encontrada"
      
      enterprise_name = enterprise.business_name
      enterprise.delete()
      return True, enterprise_name
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def get_enterprise_employees(enterprise_id, page_number=1, per_page=10, 
                              search_query='', email_query='', association_status='2'):
    """Obtener empleados de una empresa con filtros"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      enterprise_employees_ids = enterprise.employees_ids or [] if enterprise else []
      
      employees = Employee.objects.all()
      
      if search_query:
        employees = employees.filter(Q(names__icontains=search_query) | Q(last_names__icontains=search_query))
      if email_query:
        employees = employees.filter(email__icontains=email_query)
      
      if association_status == '1':
        employees = employees.filter(id__in=enterprise_employees_ids)
      elif association_status == '0':
        employees = employees.filter(id__nin=enterprise_employees_ids)
      
      employees_list = []
      for employee in employees:
        employees_list.append({
          'id': str(employee.id),
          'email': employee.email,
          'names': employee.names,
          'last_names': employee.last_names,
          'associated': str(employee.id) in [str(aid) for aid in enterprise_employees_ids]
        })
      
      total_employees = len(employees_list)
      total_pages = math.ceil(total_employees / per_page)
      offset = (page_number - 1) * per_page
      paginated_employees = employees_list[offset:offset + per_page]
      
      return {
        'employees': paginated_employees,
        'total_employees': total_employees,
        'total_pages': total_pages,
        'page_number': page_number,
        'per_page': per_page,
        'offset': offset
      }
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_enterprise_employees(enterprise_id, employees_data):
    """Actualizar empleados asociados a una empresa"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      if not enterprise:
        return False, "Empresa no encontrada"
      
      tmp = enterprise.employees_ids or []
      for employee in employees_data:
        selected = employee['selected']
        employee_id = ObjectId(employee['id'])
        if not selected and employee_id in tmp:
          tmp.remove(employee_id)
        if selected and employee_id not in tmp:
          tmp.append(employee_id)
      
      enterprise.employees_ids = list(tmp)
      enterprise.save()
      return True, None
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def get_enterprise_assets(enterprise_id, page_number=1, per_page=10, 
                           search_query='', code_query='', association_status='2'):
    """Obtener activos de una empresa con filtros"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      enterprise_assets_ids = enterprise.assets_ids or [] if enterprise else []
      
      assets = Asset.objects.all()
      
      if search_query:
        assets = assets.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
      if code_query:
        assets = assets.filter(code__icontains=code_query)
      
      if association_status == '1':
        assets = assets.filter(id__in=enterprise_assets_ids)
      elif association_status == '0':
        assets = assets.filter(id__nin=enterprise_assets_ids)
      
      assets_list = []
      for asset in assets:
        assets_list.append({
          'id': str(asset.id),
          'code': asset.code,
          'name': asset.name,
          'associated': str(asset.id) in [str(aid) for aid in enterprise_assets_ids]
        })
      
      total_assets = len(assets_list)
      total_pages = math.ceil(total_assets / per_page)
      offset = (page_number - 1) * per_page
      paginated_assets = assets_list[offset:offset + per_page]
      
      return {
        'assets': paginated_assets,
        'total_assets': total_assets,
        'total_pages': total_pages,
        'page_number': page_number,
        'per_page': per_page,
        'offset': offset
      }
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_enterprise_assets(enterprise_id, assets_data):
    """Actualizar activos asociados a una empresa"""
    try:
      enterprise = EnterpriseService.get_enterprise_by_id(enterprise_id)
      if not enterprise:
        return False, "Empresa no encontrada"
      
      tmp = enterprise.assets_ids or []
      for asset in assets_data:
        selected = asset['selected']
        asset_id = ObjectId(asset['id'])
        if not selected and asset_id in tmp:
          tmp.remove(asset_id)
        if selected and asset_id not in tmp:
          tmp.append(asset_id)
      
      enterprise.assets_ids = list(tmp)
      enterprise.save()
      return True, None
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def get_location_hierarchy(location_id):
    """Obtener jerarquía de ubicación"""
    try:
      return Location.get_district_with_hierarchy(location_id)
    except Exception:
      return None