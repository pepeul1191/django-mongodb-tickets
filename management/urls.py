from django.urls import path
from .views.index_views import home
from .views.locations_views import locations,locations_provinces , locations_districts, departments, departments_edit, departments_delete, provinces_add, provinces_edit, provinces_delete, districts_add, districts_edit, districts_delete
from .views.enterprises_views import enterprises_list, create_enterprise, update_enterprise

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
  path('enterprises/<str:enterprise_id>/delete', update_enterprise, name='delete_enterprise'),
]