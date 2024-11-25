#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create a superuser if it doesn't already exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.core.management import call_command
User = get_user_model()
if not User.objects.filter(username='davidAdmin').exists():
    User.objects.create_superuser('davidAdmin', 'paulpizarro151@gmail.com', 'con12,ro!da')
EOF