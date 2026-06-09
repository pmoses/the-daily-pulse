#!/usr/bin/env bash
set -e

cd /home/runner/workspace/news_site

echo "▶ Running migrations..."
python manage.py migrate --noinput

echo "▶ Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "▶ Ensuring superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@newssite.dev', 'admin')
    print('Superuser created — username: admin  password: admin')
else:
    print('Superuser already exists')
"

echo "▶ Seeding demo content..."
python manage.py seed_news --no-input 2>/dev/null || echo "Seed already done or skipped"

echo "▶ Starting Django on port 8000..."
python manage.py runserver 0.0.0.0:8000
