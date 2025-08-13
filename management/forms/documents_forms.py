from django import forms

class AssetDocumentForm(forms.Form):
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

  image_url = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'imageUrl'}),
    required=False
  )

  mime = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'mime'}),
    required=False
  )

  size = forms.CharField(
    widget=forms.HiddenInput(attrs={'id': 'size'}),
    required=False
  )

  created = forms.DateTimeField(required=False)