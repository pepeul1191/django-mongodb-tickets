from mongoengine import Document, ObjectIdField, StringField, DateTimeField
from datetime import datetime
from bson import ObjectId
import pytz
from pytz import timezone

class Enterprise(Document):
  """
  Modelo para representar empresas en MongoDB con soporte para UTC-5 (Perú)
  """
  
  meta = {
    'collection': 'enterprises',
    'indexes': [
      'tax_id',
      'email',
      'location_id'
    ],
    'ordering': ['-created']
  }

  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  business_name = StringField(required=True, max_length=100)
  trade_name = StringField(max_length=100)
  tax_id = StringField(required=True, regex=r'^\d{11}$')
  fiscal_address = StringField(required=True, max_length=200)
  location_id = ObjectIdField(required=True)
  phone = StringField(max_length=20)
  email = StringField(required=True, regex=r'^[^@]+@[^@]+\.[^@]+')
  website = StringField(regex=r'^https?://[^\s/$.?#].[^\s]*$')
  image_url = StringField(default='https://placehold.co/600x400/E0E0E0/333333?text=Sin+Imagen')
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def clean(self):
    self.updated = datetime.utcnow()

  def __str__(self):
    trade_name_display = f" ({self.trade_name})" if self.trade_name else ""
    return f"{self.business_name}{trade_name_display} | RUC: {self.tax_id}"

  def to_dict(self):
    return {
      'id': str(self.id),
      'businessName': self.business_name,
      'tradeName': self.trade_name,
      'taxId': self.tax_id,
      'fiscalAddress': self.fiscal_address,
      'locationId': str(self.location_id),
      'phone': self.phone,
      'email': self.email,
      'website': self.website,
      'imageUrl': self.image_url,
      'created': self.created,
      'updated': self.updated
    }

  @classmethod
  def get_by_id(cls, enterprise_id):
    try:
      return cls.objects.get(id=ObjectId(enterprise_id))
    except (cls.DoesNotExist, Exception):
      return None

