# management/services/employee_service.py
from bson import ObjectId
from mongoengine.queryset import Q
from mongoengine.errors import DoesNotExist
from datetime import datetime
import math
from management.models.employee import Employee

class EmployeeService:
  
  @staticmethod
  def get_employees_list(page_number=1, per_page=10, search_query='', email_query=''):
    """Obtener lista paginada de empleados con filtros"""
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

    employees = Employee.objects.all()
    
    query_list = []
    if search_query:
      query_list.append(Q(names__icontains=search_query) | Q(last_names__icontains=search_query))
    if email_query:
      query_list.append(Q(email__icontains=email_query))

    if query_list:
      combined_query = query_list[0]
      for q in query_list[1:]:
        combined_query &= q
      employees = employees.filter(combined_query)

    total_employees = employees.count()
    total_pages = math.ceil(total_employees / per_page)
    
    offset = (page_number - 1) * per_page
    paginated_employees = employees.skip(offset).limit(per_page)

    return {
      'employees': paginated_employees,
      'total_employees': total_employees,
      'total_pages': total_pages,
      'page_number': page_number,
      'per_page': per_page,
      'offset': offset
    }
  
  @staticmethod
  def get_employee_by_id(employee_id):
    """Obtener empleado por ID"""
    try:
      return Employee.objects.get(id=ObjectId(employee_id))
    except Employee.DoesNotExist:
      return None
    except Exception:
      return None
  
  @staticmethod
  def create_employee(names, last_names, document_number, document_type, 
                     phone, email, user_id, image_url='/user-default.png'):
    """Crear nuevo empleado"""
    try:
      employee = Employee(
        names=names,
        last_names=last_names,
        document_number=document_number,
        document_type=document_type,
        phone=phone,
        email=email,
        user_id=user_id,
        image_url=image_url
      )
      employee.save()
      return employee, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_employee(employee_id, names, last_names, document_number, 
                     document_type, phone, email, user_id, image_url):
    """Actualizar empleado existente"""
    try:
      employee = EmployeeService.get_employee_by_id(employee_id)
      if not employee:
        return None, "Empleado no encontrado"
      
      employee.names = names
      employee.last_names = last_names
      employee.document_number = document_number
      employee.document_type = document_type
      employee.phone = phone
      employee.email = email
      employee.user_id = user_id
      employee.image_url = str(image_url).strip() or '/user-default.png'
      employee.save()
      
      return employee, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_employee(employee_id):
    """Eliminar empleado"""
    try:
      employee = EmployeeService.get_employee_by_id(employee_id)
      if not employee:
        return False, "Empleado no encontrado"
      
      employee_name = employee.names
      employee.delete()
      return True, employee_name
    except Exception as e:
      return False, str(e)