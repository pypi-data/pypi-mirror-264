#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests as rq
from papamana_django.config.utils import updateconfig

def initial():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'papamana_django.config.settings')
    url = "https://env.papamana.com/api/v1/apps/env-network/"
    load_env = rq.get(url)

    if load_env.status_code == 200:
        updateconfig(list_env=load_env.json())
        print("Load environtment from network...")

def main():
    """Run administrative tasks."""
    
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
    initial()
    main()
