# Integrated Radar System (SIR)

The Integrated Radar System (SIR) is a web application that allows the configuration of the radar devices as required by the experiment,
This app allows the creation of Campaigns, Experiment and Device Configurations.
For the python3.0 update please check the requeriments vrsion for each package. It depends on the python 3.7 or 3.8 version. Special attention with the bokeh version.
For more information visit: http://jro-dev.igp.gob.pe:3000/projects/sistema-integrado-de-radar/wiki

## Installation

We recommend use docker/docker-compose for test/production but you can install the aplication as a normal django app.

### 1. Download

Download the application *radarsys* to your workspace

    $ cd /path/to/your/workspace
    $ git clone http://intranet.igp.gob.pe:8082/radarsys && cd radarsys

### 2. Build application & the migrations are already done in a .sh  
    
    $ cd /path/to/radarsys
    $ docker-compose build

### 3. Modify IP Broker

    Access to .env and modify "MQTT_SERVER" with the IP of the broker. You can install Mosquitto for this.

### 4. Run containers

    $ docker-compose up -d
