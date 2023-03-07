import os
import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio


lista_ack=[
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128
        ]



def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       #print('Connected successfully')
       mqtt_client.subscribe(os.environ.get('TOPIC_ABS_ACK','abs/beams_ack'))
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}', flush=True)
    # message= str(msg.payload)
    # sio.emit('abs_ws',data={'msg':message})
    #print("HOLA",flush=True)
    # message=msg.payload[1]
    # print("HOLAAA ",message,flush=True)
    # #lista_ack.remove(msg.payload)
    # print("LISTA     ",lista_ack)
    global lista_ack
    global lista_ack_dismatching
    message= str(msg.payload)
    message=message[2:len(message)-1]
    if(message=="UPDATE"):
        print("UUPDATE")
        sio.emit('beams_ack',data={'msg':lista_ack})
        print(lista_ack,flush=True)
        lista_ack=[
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128
        ]
    else:
        message=int(message)
        if(message<=64):
            # print(message,"\t MATCH",flush=True)
            lista_ack.remove(message+64)
            
        elif(message>64):
            # print(message,"\t DISMATCH",flush=True)
            lista_ack.remove(message-64)
        else:
            print(len(message))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(os.environ.get('MQTT_USER', 'abs'), os.environ.get('MQTT_PASSWORD', 'abs'))
client.connect(
    host=os.environ.get('MQTT_SERVER', '10.10.10.200'),
    port=int(settings.os.environ.get('MQTT_PORT', 1883)),
    keepalive=int(os.environ.get('MQTT_KEEPALIVE', 60000))
)