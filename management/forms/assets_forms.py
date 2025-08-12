from django import forms
from django.core.validators import RegexValidator, URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from main.validators import validate_object_id

class AssetForm(forms.Form):
  ESPAÑOL_ERRORS = {
    'required': 'Este campo es requerido',
    'invalid': 'Valor ingresado no válido',
  }

  id = forms.CharField(widget=forms.HiddenInput(), required=False)

  name = forms.CharField(
    label="Nombre",
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    error_messages=ESPAÑOL_ERRORS,
    required=True
  )

  description = forms.CharField(
    label="Descripción",
    max_length=2000,
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
  )

  code = forms.CharField(
    label="Código",
    max_length=50,
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
  )

  created = forms.DateTimeField(required=False)
  updated = forms.DateTimeField(required=False)