from mongoengine import Document, ObjectIdField, StringField, ReferenceField

class Location(Document):
  # Campos (en snake_case como especificas)
  name = StringField(required=True, max_length=100)  # name: String
  type = StringField(required=True, choices=["department", "province", "district"])  # type: String
  parent_id = ReferenceField('self', null=True)  # parentId: ObjectId (relación recursiva)

  # Configuración de la colección (plural y minúsculas)
  meta = {
    'collection': 'locations',  # Nombre de la colección en MongoDB
    'indexes': [
      'name',
      'parent_id'  # Index para búsquedas eficientes de jerarquías
    ]
  }

  # Método para representación legible
  def __str__(self):
    return f"{self.name} ({self.type})"