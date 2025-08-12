from mongoengine import Document, ObjectIdField, StringField, DateTimeField
from datetime import datetime
from bson import ObjectId

class Tag(Document):
  """
  Modelo para representar empresas en MongoDB con soporte para UTC-5 (Perú)
  """
  
  meta = {
    'collection': 'tags',
    'ordering': ['-created']
  }

  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  name = StringField(required=True, max_length=100)
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def clean(self):
    self.updated = datetime.utcnow()

  def __str__(self):
    return (
      f"Name: {self.name}\n"
      f"Created: {self.created.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"Updated: {self.updated.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"ID: {str(self.id)}"
    )

  def to_dict(self):
    return {
      'id': str(self.id),
      'name': self.name,
      'created': self.created,
      'updated': self.updated
    }

  @classmethod
  def get_by_id(cls, tag_id):
    try:
      return cls.objects.get(id=ObjectId(tag_id))
    except (cls.DoesNotExist, Exception):
      return None

