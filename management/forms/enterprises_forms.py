from django import forms
from django.core.validators import RegexValidator, URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from main.validators import validate_object_id

class EnterpriseForm(forms.Form):
  ESPAÑOL_ERRORS = {
    'required': 'Este campo es requerido',
    'invalid': 'Valor ingresado no válido',
  }

  id = forms.CharField(widget=forms.HiddenInput(), required=False)

  business_name = forms.CharField(
    label="Razón Social",
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    error_messages=ESPAÑOL_ERRORS,
    required=True
  )

  trade_name = forms.CharField(
    label="Nombre Comercial",
    max_length=100,
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
  )

  tax_id = forms.CharField(
    label="RUC",
    max_length=11,
    min_length=11,
    validators=[RegexValidator(r'^\d{11}$', 'El RUC debe contener exactamente 11 dígitos')],
    error_messages={
      'required': 'El RUC es obligatorio para facturación',
      'min_length': 'El RUC debe tener exactamente 11 dígitos',
      'max_length': 'El RUC debe tener exactamente 11 dígitos'
    },
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=True
  )

  phone = forms.CharField(
    label="Teléfono",
    max_length=20,
    required=False,
    widget=forms.TextInput(attrs={'class': 'form-control'})
  )

  website = forms.URLField(
    label="Sitio Web",
    required=False,
    validators=[URLValidator()],
    widget=forms.URLInput(attrs={'class': 'form-control'})
  )

  email = forms.EmailField(
    label="Correo Electrónico",
    validators=[EmailValidator()],
    widget=forms.EmailInput(attrs={'class': 'form-control'}),
    error_messages={
      'required': 'Por favor ingrese un correo válido',
      'invalid': 'Formato de correo inválido (ejemplo: nombre@empresa.com)'
    },
    required=True
  )

  location_id = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'selectedId'}),
    validators=[validate_object_id],
    error_messages={
      'required': 'La ubicación es obligatoria',
      'invalid': 'El ID de ubicación no es válido'
    },
    required=True
  )

  fiscal_address = forms.CharField(
    label="Dirección Fiscal",
    max_length=200,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=True
  )

  image_url = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'imageUrl'}),
    required=False
  )

  def clean_assets_ids(self):
    """Validación opcional para asegurar que es una lista de ObjectIds"""
    data = self.cleaned_data.get('assets_ids', [])
    if not isinstance(data, list):
      raise ValidationError("Debe ser una lista de IDs")
    return data

  def clean_employees_ids(self):
    """Validación opcional para asegurar que es una lista de ObjectIds"""
    data = self.cleaned_data.get('employees_ids', [])
    if not isinstance(data, list):
      raise ValidationError("Debe ser una lista de IDs")
    return data

  created = forms.DateTimeField(required=False)
  updated = forms.DateTimeField(required=False)