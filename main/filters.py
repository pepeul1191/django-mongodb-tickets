from django import template
from datetime import datetime
import pytz
from pytz import timezone

register = template.Library()

@register.filter
def to_datetime_local(dt, tz='America/Lima'):
  """Convierte datetime a formato 'dd/mm/aaaa h:mm:ss am/pm'"""
  if not dt or not isinstance(dt, datetime):
    return ""
  
  target_tz = timezone(tz)
  if not dt.tzinfo:
    dt = pytz.utc.localize(dt)
  
  dt_local = dt.astimezone(target_tz)
  
  # Formato completo con AM/PM
  return dt_local.strftime('%d/%m/%Y %I:%M:%S %p').lower().replace('am', 'am').replace('pm', 'pm')


@register.filter
def div(value, arg):
  try:
    return float(value) / float(arg)
  except (ValueError, ZeroDivisionError):
    return None