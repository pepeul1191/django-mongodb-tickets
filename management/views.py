from django.shortcuts import render

def index(request):
  context = {
    'page_title': 'Página Principal',
    'items': ['Item 1', 'Item 2', 'Item 3']
  }
  return render(request, 'managment/index.html', context)