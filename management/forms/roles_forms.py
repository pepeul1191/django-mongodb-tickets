from django import forms

class RoleForm(forms.Form):
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
    max_length=100,
    error_messages=ESPAÑOL_ERRORS,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
  )

  created = forms.DateTimeField(required=False)
  updated = forms.DateTimeField(required=False)