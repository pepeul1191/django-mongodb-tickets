from django.urls import path
from .views.locations import search_location

urlpatterns = [
  # locations
  path('v1/locations/search', search_location, name='search_location'),
]