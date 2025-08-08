from django.shortcuts import render

def index(request):
  context = {
    'page_title': 'Página Principal',
    'items': ['Item 1', 'Item 2', 'Item 3']
  }
  return render(request, 'main/index.html', context)

def sing_in(request):
  context = {}
  return render(request, 'main/sign-in.html', context)

def reset_password(request):
  context = {}
  return render(request, 'main/reset-password.html', context)

def handler404(request, exception):
  return render(request, '404.html', {}, status=404)