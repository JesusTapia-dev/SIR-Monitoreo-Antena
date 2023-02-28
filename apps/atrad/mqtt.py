import os
import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio
import numpy as np

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe('atrad/test3')
   else:
       print('Bad connection. Code:', rc)

def maxima_temp(trs):
    np_array = [np.array(i) for i in trs]
    temps = [max(i[i<40]) for i in np_array]
    return max(temps)

def on_message(mqtt_client, userdata, msg):
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}', flush=True)
    trsi = [[],[],[],[]]
    mensaje = str(msg.payload)
    datos = [i for i in mensaje[21:-1].split("*")]
    status=''.join([datos[i][3] for i in range(3)])
    for trs,i in zip(datos,[0,1,2,3]) :
        trsi[i]= [int(i) for i in trs[1:-1].split(",")]
    potencias = [trsi[0][34],trsi[0][36],trsi[2][32],trsi[2][34]]
    tmax = maxima_temp(trsi)
    sio.emit('test', data={'time':mensaje[2:21],'num':trsi[0][0],'pow':potencias,'tmax':str(tmax),'status':status})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(os.environ.get('MQTT_USER_ATRAD', 'atrad'), os.environ.get('MQTT_PASSWORD_ATRAD', 'atrad'))
client.connect(
    host=os.environ.get('MQTT_SERVER', '0.0.0.0'),
    port=int(settings.os.environ.get('MQTT_PORT', 1883)),
    keepalive=int(os.environ.get('MQTT_KEEPALIVE', 36000))
)