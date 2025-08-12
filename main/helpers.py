import os

def custom_urls(request):
  return {
    'BASE_URL_FROM_ENV': os.getenv('BASE_URL'),
    'FILES_URL_FROM_ENV': os.getenv('FILES_URL'),
  }

