FROM python:2.7.11

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Install python dependences
ADD requirements.txt ./requirements.txt
RUN pip install -v --timeout 120 -r requirements.txt --no-cache-dir

# Copy the main application.
COPY . ./

RUN python manage.py collectstatic --noinput


