# api/views/locations_views.py
from django.http import JsonResponse
from bson import ObjectId
from management.models.location import Location

def search_location(request):
  name = request.GET.get('name', '')
  limit = int(request.GET.get('limit', 10))
  
  try:
    results = list(Location.search_districts(name, limit))
    return JsonResponse({'data': results}, status=200)
  except Exception as e:
    return JsonResponse({'error': str(e)}, status=500)

def fetch_location(request, district_id):
  try:
    result = Location.get_district_with_hierarchy(ObjectId(district_id))
    if result:
      return JsonResponse({'data': result}, status=200)
    return JsonResponse({'error': 'Distrito no encontrado'}, status=404)
  except Exception as e:
    return JsonResponse({'error': str(e), 'message': 'ID no válido'}, status=400)