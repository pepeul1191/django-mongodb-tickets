from mongoengine import  EmbeddedDocument, ObjectIdField, StringField, DateTimeField, IntField
from datetime import datetime
from bson import ObjectId

class DocumentEmbedded(EmbeddedDocument):
  """
  Modelo embebido para documentos dentro de un Asset
  """
  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  name = StringField(required=True, max_length=100)
  description = StringField(max_length=150)
  size = IntField(required=True)
  mime = StringField(required=True, max_length=100)
  url = StringField(required=True)
  created = DateTimeField(default=datetime.utcnow)

  def __str__(self):
    return (
      f"Document: {self.name}\n"
      f"Type: {self.mime}\n"
      f"Size: {self.size} bytes\n"
      f"URL: {self.url}\n"
      f"Created: {self.created.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"ID: {str(self._id)}"
    )

  def to_dict(self):
    return {
      'id': str(self._id),
      'name': self.name,
      'description': self.description,
      'size': self.size,
      'mime': self.mime,
      'url': self.url,
      'created': self.created
    }