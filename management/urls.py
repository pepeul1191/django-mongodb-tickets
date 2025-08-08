from django.urls import path
from .views.index import home
from .views.locations import locations,locations_provinces , locations_districts, departments, departments_edit, departments_delete, districts, provinces_add, provinces_edit, provinces_delete

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
  path('locations/add/districts', districts, name='location_districts'),
]