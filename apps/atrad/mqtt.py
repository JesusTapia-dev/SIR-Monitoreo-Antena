import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio
import numpy as np
import json 
import os

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
    #    print('Connected successfullyasdss')
       mqtt_client.subscribe(os.environ.get('MQTT_TOPIC_ATRAD_RECIEVE', 'atrad/test4'))
    #    print("Exito")
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    print('Received message on topic: {} with payload: {}'.format(msg.topic,msg.payload), flush=True)
    mainData=json.loads(msg.payload)
    sio.emit('test',data = mainData)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set( '','')
client.connect(
    host=os.environ.get('MQTT_SERVER', '10.10.10.200'),
    port=int(settings.os.environ.get('MQTT_PORT', 1883)),
    keepalive=int(os.environ.get('MQTT_KEEPALIVE', 60))
)
