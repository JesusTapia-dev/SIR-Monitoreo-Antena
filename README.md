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

Create enviroment vars (/path/to/radarsys/.env)

    HOST_REDIS=radarsys-redis
    POSTGRES_DB_NAME=radarsys
    POSTGRES_PORT_5432_TCP_ADDR=radarsys-postgres
    POSTGRES_PORT_5432_TCP_PORT=5432
    POSTGRES_USER=docker
    POSTGRES_PASSWORD=****
    PGDATA=/var/lib/postgresql/data
    LC_ALL=C.UTF-8

Set database user/password in /path/to/radarsys/settings.py

### 3. Build application

    $ docker-compose build

### 4. Run containers

    $ docker-compose up -d