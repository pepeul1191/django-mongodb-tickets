from django import template
from datetime import datetime
import pytz
from pytz import timezone

register = template.Library()

@register.filter
def to_datetime_local(dt, tz='America/Lima'):
  """Convierte datetime a formato 'dd/mm/aaaa h:mm:ss am/pm'"""
  print(dt)
  if not dt or not isinstance(dt, datetime):
    return ""
  
  target_tz = timezone(tz)
  if not dt.tzinfo:
    dt = pytz.utc.localize(dt)
  
  dt_local = dt.astimezone(target_tz)
  print(dt_local)
  # Formato completo con AM/PM
  return dt_local.strftime('%Y-%m-%dT%H:%M')

@register.filter
def to_datetime_ampm(dt, tz='America/Lima'):
  """Formato legible con AM/PM (dd/mm/aaaa hh:mm AM/PM)"""
  if not dt or not isinstance(dt, datetime):
    return ""
  
  target_tz = timezone(tz)
  if not dt.tzinfo:
    dt = pytz.utc.localize(dt)
  
  dt_local = dt.astimezone(target_tz)
  # Formato 12h con AM/PM en español
  formatted = dt_local.strftime('%d/%m/%Y %I:%M %p').lower()
  return formatted.replace('am', ' a.m.').replace('pm', ' p.m.')


@register.filter
def div(value, arg):
  try:
    return float(value) / float(arg)
  except (ValueError, ZeroDivisionError):
    return None