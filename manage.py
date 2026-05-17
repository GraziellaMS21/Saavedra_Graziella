#!/usr/bin/env python
"""Thin wrapper to run the Django project located in the Django Project subfolder."""
import os
import sys

PROJECT_SUBDIR = 'Django Project'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_SUBDIR)

if __name__ == '__main__':
    os.chdir(PROJECT_DIR)
    sys.path.insert(0, PROJECT_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
