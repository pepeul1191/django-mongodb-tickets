from django import template
from datetime import datetime
import pytz
from pytz import timezone

register = template.Library()

@register.filter
def to_datetime_local(dt, tz='America/Lima'):
  """Convierte datetime a formato para input datetime-local"""
  if not dt or not isinstance(dt, datetime):
    return ""
  
  target_tz = timezone(tz)
  if not dt.tzinfo:
    dt = pytz.utc.localize(dt)
  
  return dt.astimezone(target_tz).strftime('%Y-%m-%dT%H:%M')