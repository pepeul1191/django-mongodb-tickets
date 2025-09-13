from django.shortcuts import render
from main.decorators import auth_required, auth_required_inverse

@auth_required
def home(request):
  context = {
    'page_title': 'Página Principal',
    'nav_link': '',
  }
  return render(request, 'management/index.html', context)