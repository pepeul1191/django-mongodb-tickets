from mongoengine import Document, EmbeddedDocument, ObjectIdField, StringField, DateTimeField, ListField, EmbeddedDocumentField
from datetime import datetime
from bson import ObjectId
from .document_embedded import DocumentEmbedded

class Asset(Document):
  """
  Modelo para representar activos en MongoDB
  """
  meta = {
    'collection': 'assets',
    'ordering': ['-created']
  }

  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  name = StringField(required=True, max_length=100)
  code = StringField(required=True, max_length=50, unique=True)
  description = StringField(max_length=2000)
  documents = ListField(EmbeddedDocumentField(DocumentEmbedded))
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def clean(self):
    self.updated = datetime.utcnow()

  def __str__(self):
    return (
      f"Asset: {self.name}\n"
      f"Code: {self.code}\n"
      f"Description: {self.description or 'No description'}\n"
      f"Documents: {len(self.documents)} attached\n"
      f"Created: {self.created.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"Updated: {self.updated.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"ID: {str(self._id)}"
    )

  def to_dict(self):
    return {
      'id': str(self._id),
      'name': self.name,
      'code': self.code,
      'description': self.description,
      'documents': [doc.to_dict() for doc in self.documents],
      'created': self.created,
      'updated': self.updated
    }

  @classmethod
  def get_by_id(cls, asset_id):
    try:
      return cls.objects.get(_id=ObjectId(asset_id))
    except (cls.DoesNotExist, Exception):
      return None

  @classmethod
  def get_by_code(cls, code):
    try:
      return cls.objects.get(code=code)
    except (cls.DoesNotExist, Exception):
      return None