FROM bitnami/minideb:jessie

# setup libraries
RUN install_packages python --timeout 120 \
                     python-pip --timeout 120 \
                     python-dev --timeout 120 \
                     gfortran --timeout 120 \
                     libpng-dev --timeout 120 \ 
                     freetype* --timeout 120 \
                     libblas-dev --timeout 120 \
                     liblapack-dev --timeout 120 \
                     libmysqlclient-dev --timeout 120 \
                     libatlas-base-dev --timeout 120

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Copy the main application.
COPY . ./

# Install python dependences
RUN pip install -v --timeout 120 -r requirements.txt

RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py loaddata apps/main/fixtures/main_initial_data.json \
    && python manage.py loaddata apps/rc/fixtures/rc_initial_data.json \
    && python manage.py loaddata apps/jars/fixtures/jars_initial_data.json

EXPOSE 3000
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]

