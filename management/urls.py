from django.urls import path
from .views.index import home
from .views.locations import locations,locations_provinces , locations_districts

urlpatterns = [
  path('', home, name='managment_index'),
  path('locations/', locations, name='subapp_index'),
  path('locations/<str:department_id>/provinces/', locations_provinces, name='location_provinces'),
  path('locations/<str:department_id>/provinces/<str:province_id>/districts', locations_districts, name='location_districts'),
]