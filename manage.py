#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_academica.settings')

    # Lógica para crear superusuario automáticamente
    if os.environ.get('CREATE_SUPERUSER', None):
        try:
            import django
            django.setup()
            from django.contrib.auth.models import User

            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'adminDavid')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'paulpizarro151@gamil.com')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'con12,ro!da')

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f"Superuser {username} created successfully!")
            else:
                print(f"Superuser {username} already exists.")
        except Exception as e:
            print(f"Error creating superuser: {e}")

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
