from mongoengine import  EmbeddedDocument, ObjectIdField, StringField, DateTimeField, IntField
from datetime import datetime
from bson import ObjectId

class UserEmbedded(EmbeddedDocument):
  """
  Modelo embebido para documentos dentro de un Asset
  """
  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  username = StringField(required=True, max_length=100)
  user_id = IntField(required=True)
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def __str__(self):
    return (
      f"User: {self.username}\n"
      f"User ID: {self.user_id}\n"
      f"Created: {self.created.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"Updated: {self.updated.strftime('%Y-%m-%d %H:%M')} (UTC)\n"
      f"ID: {str(self.id)}"
    )

  def to_dict(self):
    return {
      'id': str(self.id),
      'username': self.username,
      'user_id': self.user_id,
      'created': self.created.isoformat() if self.created else None,
      'updated': self.updated.isoformat() if self.updated else None
    }

  meta = {
    'indexes': [
      'user_id',
      'username'
    ]
  }