from django import forms
from django.core.validators import RegexValidator, URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from main.validators import validate_object_id
from management.models.employee import Employee

class EmployeeForm(forms.Form):
  ESPAÑOL_ERRORS = {
    'required': 'Este campo es requerido',
    'invalid': 'Valor ingresado no válido',
  }

  id = forms.CharField(widget=forms.HiddenInput(), required=False)

  names = forms.CharField(
    label="Nombre",
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    error_messages=ESPAÑOL_ERRORS,
    required=True
  )

  last_names = forms.CharField(
    label="Apellidos",
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    error_messages=ESPAÑOL_ERRORS,
    required=True
  )

  document_number = forms.CharField(
    label="Número de Documento",
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
  )

  document_type = forms.ChoiceField(
    choices=Employee.DOCUMENT_TYPES,  # Usa las opciones del modelo
    label="Tipo de documento",
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.Select(attrs={
        'class': 'form-control',  # Clases CSS (opcional)
    })
  )

  phone = forms.CharField(
    label="Teléfono",
    max_length=20,
    required=False,
    widget=forms.TextInput(attrs={'class': 'form-control'})
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

  user_id = forms.CharField(widget=forms.HiddenInput(), required=False)

  image_url = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'imageUrl'}),
    required=False,
    initial='/user-default.png'  # Valor por defecto
  )


  def clean_image_url(self):
    image_url = self.cleaned_data.get('image_url', '').strip()
    if len(image_url) == 0:
      return '/user-default.png'
    else:
      return image_url

  created = forms.DateTimeField(required=False)
  updated = forms.DateTimeField(required=False)