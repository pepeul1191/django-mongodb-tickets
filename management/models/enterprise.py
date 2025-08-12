from mongoengine import Document, ObjectIdField, StringField, DateTimeField
from datetime import datetime
from bson import ObjectId

class Enterprise(Document):
  """
  Modelo para representar empresas en la base de datos MongoDB
  """
  
  meta = {
    'collection': 'enterprises',
    'indexes': [
      'tax_id',
      'email',
      'location_id'
    ]
  }

  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  business_name = StringField(required=True, max_length=100)  # Razón social
  trade_name = StringField(max_length=100)  # Nombre comercial
  tax_id = StringField(required=True, regex=r'^\d{11}$')  # RUC peruano
  fiscal_address = StringField(required=True, max_length=200)
  location_id = ObjectIdField(required=True)
  phone = StringField(max_length=20)
  email = StringField(required=True, regex=r'^[^@]+@[^@]+\.[^@]+')
  website = StringField(regex=r'^https?://[^\s/$.?#].[^\s]*$')
  image_url = StringField()
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def clean(self):
    """Actualiza automáticamente la fecha de modificación"""
    self.updated = datetime.utcnow()

  def __str__(self):
    """Representación legible del objeto"""
    trade_name_info = f" ({self.trade_name})" if self.trade_name else ""
    location_info = f" - Loc: {str(self.location_id)[:8]}..." if self.location_id else ""
    contact_info = f" | ✉ {self.email}" if self.email else ""
    phone_info = f" | ☎ {self.phone}" if self.phone else ""
    
    return (
      f"{self.business_name}{trade_name_info} "
      f"[RUC: {self.trade_name}]{location_info}"
      f"{contact_info}{phone_info}"
    )

  def to_dict(self):
    """Convierte el modelo a diccionario para APIs"""
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
      'created': self.created.isoformat(),
      'updated': self.updated.isoformat()
    }