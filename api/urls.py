from django.urls import path
from .views.locations_views import search_location, fetch_location

urlpatterns = [
  # locations
  path('v1/locations/search', search_location, name='search_location'),
  path('v1/locations/<str:district_id>', fetch_location, name='fetch_location'),
]