from django.shortcuts import render

def home(request):
  context = {
    'page_title': 'Página Principal',
    'nav_link': '',
  }
  return render(request, 'management/index.html', context)