FROM bitnami/minideb:jessie

# setup libraries
RUN install_packages python \
                     python-pip \
                     python-dev \
                     gfortran \
                     libpng-dev \ 
                     freetype* \
                     libblas-dev \
                     liblapack-dev \
                     libatlas-base-dev
# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Copy the main application.
COPY . ./

# Install python dependences
RUN pip install -r requirements.txt
RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py loaddata apps/main/fixtures/main_initial_data.json \
    && python manage.py loaddata apps/rc/fixtures/rc_initial_data.json \
    && python manage.py loaddata apps/jars/fixtures/jars_initial_data.json

EXPOSE 3000
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]

