FROM python:3.11.1-slim

# set working directory
RUN mkdir /radarsys
RUN pwd
WORKDIR /radarsys
COPY /pipLibraries ./
RUN pwd
RUN ls -al

# Install python dependences
ADD requirements.txt ./requirements.txt
RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends \
	gcc \
    g++ \
    && pip install -v --timeout 120 --no-cache-dir ./Django-4.1.5-py3-none-any.whl \
    && pip install -v --timeout 120 --no-cache-dir ./django-bootstrap5-22.2.tar.gz \
    && pip install -v --timeout 120 --no-cache-dir ./psycopg_binary-3.1.8-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && pip install -v --timeout 120 --no-cache-dir ./django-polymorphic-3.1.0.tar.gz \
    && pip install -v --timeout 120 --no-cache-dir ./numpy-1.24.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && pip install -v --timeout 120 --no-cache-dir ./bokeh-3.0.3-py3-none-any.whl\
    && pip install -v --timeout 120 --no-cache-dir ./matplotlib-3.6.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && pip install -v --timeout 120 --no-cache-dir ./scipy-1.10.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && pip install -v --timeout 120 --no-cache-dir ./celery-5.2.7.tar.gz \
    && pip install -v --timeout 120 --no-cache-dir ./gunicorn-20.1.0-py3-none-any.whl \
    && pip install -v --timeout 120 --no-cache-dir ./requests-2.28.2-py3-none-any.whl \
    && pip install -v --timeout 120 --no-cache-dir ./redis-4.4.2-py3-none-any.whl \
    && pip install -v --timeout 120 --no-cache-dir ./graphene_django-3.0.0-py2.py3-none-any.whl \
#&& pip install -v --timeout 120 -r requirements.txt --no-cache-dir \
    && apt-get purge -y --auto-remove gcc g++\
	&& rm -rf /var/lib/apt/lists/*

# Copy the main application.
COPY . ./

EXPOSE 8000

