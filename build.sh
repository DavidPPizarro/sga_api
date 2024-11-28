#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

#python populate.py
# Create superuser
python <<EOF
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_academica.settings")  # Reemplaza "tu_proyecto" con el nombre de tu proyecto
django.setup()

User = get_user_model()

# Superuser credentials
email = "admin@example.com"  # Reemplaza con el correo deseado
password = "12345"  # Reemplaza con la contraseña deseada

# Check if the superuser already exists
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print(f"Superuser created: {email}")
else:
    print(f"Superuser with email {email} already exists.")
EOF