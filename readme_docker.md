# Commands after dockers creations

docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py loaddata apps/main/fixtures/main_initial_data.json \
docker-compose run web python manage.py loaddata apps/rc/fixtures/rc_initial_data.json \
docker-compose run web python manage.py loaddata apps/jars/fixtures/initial_filters_data.json \
docker-compose run web python manage.py collectstatic
