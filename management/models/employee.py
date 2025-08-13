from mongoengine import Document, ObjectIdField, StringField, DateTimeField, ValidationError
from datetime import datetime
from bson import ObjectId

class Employee(Document):
  """
  Modelo para representar empleados en MongoDB con validación de documentos.
  """
  
  meta = {
    'collection': 'employees',
    'ordering': ['-created']
  }

  DOCUMENT_TYPES = (
    ('DNI', 'DNI'),
    ('CE', 'C. de Extranjería'),
    ('PAS', 'Pasaporte'),
  )

  id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
  names = StringField(required=True, max_length=100)
  last_names = StringField(max_length=100, required=True)
  document_number = StringField(required=True, max_length=15)  # Validación manual en clean()
  document_type = StringField(required=True, choices=DOCUMENT_TYPES)
  phone = StringField(max_length=25)
  email = StringField(required=True, regex=r'^[^@]+@[^@]+\.[^@]+')
  user_id = StringField(max_length=30, default='')
  image_url = StringField(default='/user-default.png')
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(default=datetime.utcnow)

  def clean(self):
    self.updated = datetime.utcnow()
    super().clean()
    
    if self.document_type == 'DNI':
      if not self.document_number.isdigit() or len(self.document_number) != 8:
        raise ValidationError("DNI debe tener 8 dígitos numéricos.")
    
    elif self.document_type == 'CE':
      if len(self.document_number) < 9 or len(self.document_number) > 12:
        raise ValidationError("Carné de Extranjería debe tener 9-12 caracteres.")
      if not self.document_number.isalnum():
        raise ValidationError("Carné de Extranjería debe ser alfanumérico.")
    
    elif self.document_type == 'PAS':
      if len(self.document_number) < 6 or len(self.document_number) > 12:
        raise ValidationError("Pasaporte debe tener 6-12 caracteres.")
      if not self.document_number.isalnum():
        raise ValidationError("Pasaporte debe ser alfanumérico.")

  def __str__(self):
    return f"Employee: {self.names} {self.last_names} ({self.document_type}: {self.document_number})"

  def to_dict(self):
    return {
      "id": str(self.id),
      "names": self.names,
      "last_names": self.last_names,
      "document_type": self.document_type,
      "document_number": self.document_number,
      "phone": self.phone,
      "email": self.email,
      "user_id": self.user_id,
      "image_url": self.image_url,
      "created": self.created.isoformat(),
      "updated": self.updated.isoformat()
    }


  @classmethod
  def get_by_id(cls, enterprise_id):
    try:
      return cls.objects.get(id=ObjectId(enterprise_id))
    except (cls.DoesNotExist, Exception):
      return None

