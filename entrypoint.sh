#!/bin/sh
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py loaddata apps/main/fixtures/main_initial_data.json 
python3 manage.py loaddata apps/rc/fixtures/rc_initial_data.json 
python3 manage.py loaddata apps/jars/fixtures/initial_filters_data.json 
python3 manage.py collectstatic --no-input 

#DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

gunicorn radarsys.wsgi:application -w 2 -b :8000
 