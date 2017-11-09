FROM bitnami/minideb:jessie

# setup libraries
RUN install_packages python --fix-missing \
                     python-pip --fix-missing \
                     python-dev --fix-missing \
                     gfortran --fix-missing \
                     libpng-dev --fix-missing \ 
                     freetype* --fix-missing \
                     libblas-dev --fix-missing \
                     liblapack-dev --fix-missing \
                     libmysqlclient-dev --fix-missing \
                     libatlas-base-dev --fix-missing

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

