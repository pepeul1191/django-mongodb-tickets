from django.urls import path
from .views.index_views import home
from .views.locations_views import locations,locations_provinces , locations_districts, departments, departments_edit, departments_delete, provinces_add, provinces_edit, provinces_delete, districts_add, districts_edit, districts_delete
from .views.enterprises_views import enterprises_list, create_enterprise, update_enterprise, delete_enterprise, emplolyees_enterprise, assets_enterprise
from .views.roles_views import roles_list, create_role, update_role, delete_role
from .views.tags_views import tags_list, create_tag, update_tag, delete_tag
from .views.assets_views import assets_list, create_asset, update_asset, delete_asset, asset_add_document, asset_delete_document
from .views.employees_views import employees_list, create_employee, update_employee, delete_employee

urlpatterns = [
  path('', home, name='managment_index'),
  # locations
  path('locations/', locations, name='locations'),
  # locations - departments
  path('locations/departments', departments, name='location_departments'),
  path('locations/<str:department_id>/edit', departments_edit, name='departments_edit'),
  path('locations/<str:department_id>/delete', departments_delete, name='departments_delete'),
  # locations - provinces
  path('locations/<str:department_id>/provinces/', locations_provinces, name='location_provinces'),
  path('locations/<str:department_id>/provinces/add', provinces_add, name='provinces_add'),
  path('locations/<str:department_id>/provinces/<str:province_id>/edit', provinces_edit, name='provinces_edit'),
  path('locations/<str:department_id>/provinces/<str:province_id>/delete', provinces_delete, name='provices_delete'),
  # locations - districts
  path('locations/<str:department_id>/provinces/<str:province_id>/districts', locations_districts, name='location_districts'),
  path('locations/<str:department_id>/provinces/<str:province_id>/districts/add', districts_add, name='location_districts'),
  path('locations/<str:department_id>/provinces/<str:province_id>/districts/<str:district_id>/edit', districts_edit, name='location_districts'),
  path('locations/<str:department_id>/provinces/<str:province_id>/districts/<str:district_id>/delete', districts_delete, name='districts_delete'),
  # enterprises
  path('enterprises/', enterprises_list, name='enterprises_list'),
  path('enterprises/add', create_enterprise, name='enterprises_add'),
  path('enterprises/<str:enterprise_id>', update_enterprise, name='enterprise_detail'),
  path('enterprises/<str:enterprise_id>/edit', update_enterprise, name='update_enterprise'),
  path('enterprises/<str:enterprise_id>/delete', delete_enterprise, name='delete_enterprise'),
  path('enterprises/<str:enterprise_id>/employees', emplolyees_enterprise, name='emplolyees_enterprise'),
  path('enterprises/<str:enterprise_id>/assets', assets_enterprise, name='assets_enterprise'),
  # roles
  path('roles/', roles_list, name='roles_list'),
  path('roles/add', create_role, name='roles_add'),
  path('roles/<str:role_id>', update_role, name='role_detail'),
  path('roles/<str:role_id>/edit', update_role, name='update_role'),
  path('roles/<str:role_id>/delete', delete_role, name='delete_role'),
  # tags
  path('tags/', tags_list, name='tags_list'),
  path('tags/add', create_tag, name='tags_add'),
  path('tags/<str:tag_id>', update_tag, name='tag_detail'),
  path('tags/<str:tag_id>/edit', update_tag, name='update_tag'),
  path('tags/<str:tag_id>/delete', delete_tag, name='delete_tag'),
  # assets
  path('assets/', assets_list, name='assets_list'),
  path('assets/add', create_asset, name='assets_add'),
  path('assets/<str:asset_id>', update_asset, name='asset_detail'),
  path('assets/<str:asset_id>/edit', update_asset, name='update_asset'),
  path('assets/<str:asset_id>/delete', delete_asset, name='delete_asset'),
  path('assets/<str:asset_id>/document', asset_add_document, name='asset_add_document'),
  path('assets/<str:asset_id>/document/<str:document_id>/delete', asset_delete_document, name='asset_delete_document'),
   # employees
  path('employees/', employees_list, name='employees_list'),
  path('employees/add', create_employee, name='employees_add'),
  path('employees/<str:employee_id>', update_employee, name='employee_detail'),
  path('employees/<str:employee_id>/edit', update_employee, name='update_employee'),
  path('employees/<str:employee_id>/delete', delete_employee, name='delete_employee'),
]