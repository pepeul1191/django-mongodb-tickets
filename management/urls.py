from django.urls import path
from .views.index import home
from .views.locations import locations,locations_provinces , locations_districts, departments, departments_edit, departments_delete, provinces, districts

urlpatterns = [
  path('', home, name='managment_index'),
  path('locations/', locations, name='locations'),
  path('locations/<str:department_id>/provinces/', locations_provinces, name='location_provinces'),
  path('locations/<str:department_id>/provinces/<str:province_id>/districts', locations_districts, name='location_districts'),
  path('locations/<str:department_id>/edit', departments_edit, name='departments_edit'),
  path('locations/<str:department_id>/delete', departments_delete, name='departments_delete'),
  path('locations/departments', departments, name='location_departments'),
  path('locations/add/provinces', provinces, name='location_provinces'),
  path('locations/add/districts', districts, name='location_districts'),
]