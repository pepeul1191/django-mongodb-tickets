from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from management.models import Location 
from mongoengine.errors import DoesNotExist
from management.forms.locations_forms import LocationForm

nav_link = 'enterprises'

def enterprises(request):
  if request.method == 'GET':
    departments = Location.objects.filter(type="department")

    context = {
      'page_title': 'Gestión de Empresas',
      'nav_link': nav_link,
      #'departments': departments,
    }

    return render(request, 'management/enterprises/index.html', context)
  else:
    return JsonResponse({
        'status': 'form_error',
        'errors': 'XD'
    }, status=400)
  

def enterprises_add(request):
  if request.method == 'GET':
    context = {
      'page_title': 'Gestión de Empresas',
      'nav_link': nav_link,
    }

    return render(request, 'management/enterprises/detail.html', context)
  else:
    return JsonResponse({
        'status': 'form_error',
        'errors': 'XD'
    }, status=400)