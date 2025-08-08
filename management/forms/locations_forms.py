from django import forms
from django.core.exceptions import ValidationError
from bson import ObjectId
from bson.errors import InvalidId

class LocationForm(forms.Form):
  id = forms.CharField(required=False, widget=forms.HiddenInput())
  name = forms.CharField(max_length=100, required=True)
  parent_id = forms.CharField(required=False, widget=forms.HiddenInput())

  def clean_id(self):
    """Convierte el string a ObjectId"""
    id_value = self.cleaned_data.get('id')
    if id_value:
      try:
        return ObjectId(id_value)
      except InvalidId:
        raise forms.ValidationError("ID inválido")
    return None

  def clean_parent_id(self):
    """Valida parent_id si existe"""
    parent_id = self.cleaned_data.get('parent_id')
    if parent_id:
      try:
        return ObjectId(parent_id)
      except InvalidId:
        raise forms.ValidationError("ID padre inválido")
    return None