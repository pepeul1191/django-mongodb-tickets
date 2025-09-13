from mongoengine import Document, StringField, ReferenceField
from bson import ObjectId
from mongoengine.queryset.visitor import Q

class Location(Document):
  name = StringField(required=True, max_length=100)
  type = StringField(required=True, choices=["department", "province", "district"])
  parent_id = ReferenceField('self', null=True)

  meta = {
    'collection': 'locations',
    'indexes': [
      {
        'fields': ['name'],
        'name': 'name_es_collation',
        'collation': {'locale': 'es', 'strength': 2}
      },
      {
        'fields': ['type'],
        'name': 'type_index'
      },
      {
        'fields': ['parent_id'],
        'name': 'parent_id_index'
      }
    ]
  }

  @classmethod
  def search_districts(cls, name, limit=10):
    """
    Busca distritos por nombre con su jerarquía completa
    Args:
      name (str): Texto a buscar
      limit (int): Límite de resultados
    Returns:
      list: Lista de distritos con su jerarquía
    """
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
          "$concat": [
            "$name", ", ",
            "$province", ", ",
            "$department"
          ]
        }
      }},
      {"$match": {
        "full_name": {"$regex": name, "$options": "i"}
      }},
      {"$project": {
        "_id": 0,
        "district_id": {"$toString": "$_id"},
        "name": "$name",
        "province_name": "$province",
        "district_name": "$name",
        "full_name": 1  # Se agrega full_name con la concatenación
      }},
      {"$limit": limit}
    ]
    return cls.objects.aggregate(pipeline)

  @classmethod
  def get_district_with_hierarchy(cls, district_id):
    """
    Obtiene un distrito con su jerarquía completa
    Args:
      district_id (str|ObjectId): ID del distrito
    Returns:
      dict: Datos del distrito con su jerarquía
    """
    pipeline = [
      {
        "$match": {
          "_id": district_id,
          "type": "district"
        }
      },
      {
        "$graphLookup": {
          "from": "locations",
          "startWith": "$parent_id",
          "connectFromField": "parent_id",
          "connectToField": "_id",
          "as": "ancestors",
          "maxDepth": 2
        }
      },
      {
        "$addFields": {
          "province": {
            "$arrayElemAt": [
              {
                "$filter": {
                  "input": "$ancestors",
                  "as": "a",
                  "cond": {"$eq": ["$$a.type", "province"]}
                }
              },
              0
            ]
          },
          "department": {
            "$arrayElemAt": [
              {
                "$filter": {
                  "input": "$ancestors",
                  "as": "a",
                  "cond": {"$eq": ["$$a.type", "department"]}
                }
              },
              0
            ]
          }
        }
      },
      {
        "$addFields": {
          "full_name": {
            "$concat": [
              "$name", ", ",
              "$province.name", ", ",
              "$department.name"
            ]
          }
        }
      },
      {
        "$project": {
          "_id": 0,
          "district_id": {"$toString": "$_id"},
          "name": "$name",
          "province_name": "$province.name",
          "district_name": "$name",
          "full_name": 1  # Se agrega full_name con la concatenación
        }
      }
    ]
    try:
      result = cls.objects.aggregate(pipeline).next()
      return result
    except (StopIteration, Exception):
      return None

  def get_hierarchy(self):
    """
    Obtiene la jerarquía completa para la ubicación actual
    Returns:
      dict: Diccionario con la jerarquía
    """
    if self.type == 'department':
      return {
        'department': self.name,
        'province': None,
        'district': None
      }
    elif self.type == 'province':
      return {
        'department': self.parent_id.name if self.parent_id else None,
        'province': self.name,
        'district': None
      }
    else:  # district
      province = Location.objects.filter(
        id=self.parent_id.id,
        type='province'
      ).first()
      department = province.parent_id if province else None

      return {
        'department': department.name if department else None,
        'province': province.name if province else None,
        'district': self.name
      }
