# En tu archivo forms.py o validators.py
from bson import ObjectId
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_object_id(value):
  """
  Valida que el valor sea un ObjectId de MongoDB válido
  """
  try:
    ObjectId(value)
  except:
    raise ValidationError(
      _('%(value)s no es un ObjectId válido'),
      params={'value': value},
    )