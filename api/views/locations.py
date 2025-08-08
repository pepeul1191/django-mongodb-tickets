from mongoengine import get_db
from bson.objectid import ObjectId
from django.http import JsonResponse
from main.database import init_db # Asume que database.py está en tu_app
import re

def search_location(request):
  name = request.GET.get('name', '')
  limit = int(request.GET.get('limit', 10))
  
  try:
    db = get_db()

    pipeline = [
      {"$match": {"type": "district"}},
      {"$graphLookup": {
        "from": "locations",
        "startWith": "$parent_id",
        "connectFromField": "parent_id",
        "connectToField": "_id",
        "as": "ancestors"
      }},
      {"$addFields": {
        "province": {
          "$first": {
            "$map": {
              "input": {
                "$filter": {
                  "input": "$ancestors",
                  "as": "a",
                  "cond": {"$eq": ["$$a.type", "province"]}
                }
              },
              "as": "prov",
              "in": "$$prov.name"
            }
          }
        },
        "department": {
          "$first": {
            "$map": {
              "input": {
                "$filter": {
                  "input": "$ancestors",
                  "as": "a",
                  "cond": {"$eq": ["$$a.type", "department"]}
                }
              },
              "as": "dep",
              "in": "$$dep.name"
            }
          }
        }
      }},
      {"$addFields": {
        "full_name": {
          "$concat": ["$name", ", ", "$province", ", ", "$department"]
        }
      }},
      {"$match": {
        "full_name": {"$regex": name, "$options": "i"}
      }},
      {"$project": {
        "_id": 0,
        "district_id": {"$toString": "$_id"},
        "full_name": 1
      }},
      {"$limit": limit}
    ]
    
    results = list(db.locations.aggregate(pipeline))
    return JsonResponse({'data': results}, status=200)
    
  except Exception as e:
    return JsonResponse({'error': str(e)}, status=500)