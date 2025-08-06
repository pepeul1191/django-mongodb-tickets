#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def ensure_uploads_dir_exists():
    """Ensure the uploads directory exists."""
    uploads_dir = Path(__file__).parent / 'uploads'
    try:
        uploads_dir.mkdir(exist_ok=True)
        print(f"Verified uploads directory at: {uploads_dir}")
    except Exception as e:
        print(f"Error creating uploads directory: {e}")

def main():
    """Run administrative tasks."""
    # Ensure uploads directory exists before doing anything else
    ensure_uploads_dir_exists()
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()