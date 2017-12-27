FROM python:2.7.11

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Install python dependences
ADD requirements.txt ./requirements.txt
RUN pip install -v --timeout 120 -r requirements.txt --no-cache-dir

# Copy the main application.
COPY . ./
#RUN mkdir /radarsys media
# RUN python manage.py makemigrations \
#  && python manage.py migrate \
#  && python manage.py loaddata apps/main/fixtures/main_initial_data.json \
#  && python manage.py loaddata apps/rc/fixtures/rc_initial_data.json \
#  && python manage.py loaddata apps/jars/fixtures/initial_filters_data.json \
RUN python manage.py collectstatic --noinput
#EXPOSE 3000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
# Para produccion:
#CMD ["gunicorn", "radarsys.wsgi:application", "--bind", "0.0.0.0:3000"]

