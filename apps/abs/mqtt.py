import os
import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio

lista_ack=[
    chr( 33 ), chr( 34 ), chr( 35 ), chr( 36 ), chr( 37 ), chr( 38 ), chr( 39 ), chr( 40 ), chr( 41 ), chr( 42 ), chr( 43 ), chr( 44 ), chr( 45 ), chr( 46 ), chr( 47 ), chr( 48 ), chr( 49 ), chr( 50 ), chr( 51 ), chr( 52 ), chr( 53 ), chr( 54 ), chr( 55 ), chr( 56 ), chr( 57 ), chr( 58 ), chr( 59 ), chr( 60 ), chr( 61 ), chr( 62 ), chr( 63 ), chr( 64 ), chr( 65 ), chr( 66 ), chr( 67 ), chr( 68 ), chr( 69 ), chr( 70 ), chr( 71 ), chr( 72 ), chr( 73 ), chr( 74 ), chr( 75 ), chr( 76 ), chr( 77 ), chr( 78 ), chr( 79 ), chr( 80 ), chr( 81 ), chr( 82 ), chr( 83 ), chr( 84 ), chr( 85 ), chr( 86 ), chr( 87 ), chr( 88 ), chr( 89 ), chr( 90 ), chr( 91 ), chr( 92 ), chr( 93 ), chr( 94 ), chr( 95 ), chr( 96 )
    ]

lista_ack_dismatching=[
    chr( 97 ), chr( 98 ), chr( 99 ), chr( 100 ), chr( 101 ), chr( 102 ), chr( 103 ), chr( 104 ), chr( 105 ), chr( 106 ), chr( 107 ), chr( 108 ), chr( 109 ), chr( 110 ), chr( 111 ), chr( 112 ), chr( 113 ), chr( 114 ), chr( 115 ), chr( 116 ), chr( 117 ), chr( 118 ), chr( 119 ), chr( 120 ), chr( 121 ), chr( 122 ), chr( 123 ), chr( 124 ), chr( 125 ), chr( 126 ), chr( 127 ), chr( 128 ), chr( 129 ), chr( 130 ), chr( 131 ), chr( 132 ), chr( 133 ), chr( 134 ), chr( 135 ), chr( 136 ), chr( 137 ), chr( 138 ), chr( 139 ), chr( 140 ), chr( 141 ), chr( 142 ), chr( 143 ), chr( 144 ), chr( 145 ), chr( 146 ), chr( 147 ), chr( 148 ), chr( 149 ), chr( 150 ), chr( 151 ), chr( 152 ), chr( 153 ), chr( 154 ), chr( 155 ), chr( 156 ), chr( 157 ), chr( 158 ), chr( 159 ), chr(160)
]

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(os.environ.get('TOPIC_ABS_ACK','abs/beams_ack'))
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}', flush=True)
    # message= str(msg.payload)
    # sio.emit('abs_ws',data={'msg':message})
    #message=str(msg.payload)
    #lista_ack.pop(message)
    print("Mientras"   ,flush=True)

    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(os.environ.get('MQTT_USER', 'abs'), os.environ.get('MQTT_PASSWORD', 'abs'))
client.connect(
    host=os.environ.get('MQTT_SERVER', '10.10.10.200'),
    port=int(settings.os.environ.get('MQTT_PORT', 1883)),
    keepalive=int(os.environ.get('MQTT_KEEPALIVE', 36000))
)