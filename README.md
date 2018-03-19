# Integrated Radar System (SIR)

The Integrated Radar System (SIR) is a web application that allows the configuration of the radar devices as required by the experiment,
This app allows the creation of Campaigns, Experiment and Device Configurations.
For more information visit: http://jro-dev.igp.gob.pe:3000/projects/sistema-integrado-de-radar/wiki

## Installation

We recommend use docker/docker-compose for test/production but you can install the aplication as a normal django app.

### 1. Download

Download the application *radarsys* to your workspace

    $ cd /path/to/your/workspace
    $ git clone http://jro-dev.igp.gob.pe/rhodecode/radarsys && cd radarsys

### 2. Config app

Update enviroment vars (/path/to/radarsys/.env)

    REDIS_HOST=radarsys-redis
    REDIS_PORT=6300
    POSTGRES_DB_NAME=radarsys
    POSTGRES_PORT_5432_TCP_ADDR=radarsys-postgres
    POSTGRES_PORT_5432_TCP_PORT=5400
    POSTGRES_USER=docker
    POSTGRES_PASSWORD=****
    PGDATA=/var/lib/postgresql/data
    LC_ALL=C.UTF-8

### 3. Build application & make migrations (only once at installation) 

    $ cd /path/to/radarsys
    $ docker-compose build
    $ docker-compose run web python manage.py makemigrations
    $ docker-compose run web python manage.py migrate
    $ docker-compose run web python manage.py loaddata apps/main/fixtures/main_initial_data.json 
    $ docker-compose run web python manage.py loaddata apps/rc/fixtures/rc_initial_data.json
    $ docker-compose run web python manage.py loaddata apps/jars/fixtures/initial_filters_data.json
    $ docker-compose run web python manage.py collectstatic

### 4. Run containers

    $ docker-compose up -d
