import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio
import numpy as np
import psycopg2
import os

def insert(time,data):
    sql = """INSERT INTO atrad_datas(
        datetime,nstx,status,temp_cll,nboards,tempdvr,potincdvr,potretdvr,
        temp1,potinc1,potret1,temp2,potinc2,potret2,temp3,potinc3,potret3,
        temp4,potinc4,potret4,temp5,potinc5,potret5,temp6,potinc6,potret6)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(database="radarsys", user='docker', password='docker', host='radarsys-postgres', port= '5432')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        #data_tuple = [tuple(i[:]) for i in a]
        values = (time,) + tuple(data[0][:25])
        cur.execute(sql, values)

        # get the generated id back
        #vendor_id = cur.fetchone()[0]
        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def maxTemperature(trs):
    temps = GetTemperatures(trs)
    maxT_STX = [max(i) for i in temps]
    maxT = max(maxT_STX)
    STXnum = maxT_STX.index(maxT)
    STXloc = temps[STXnum].index(maxT)
    maxT_loc = 'Amp ' + str(STXnum+1)

    if STXloc == 0:
        maxT_loc = maxT_loc + " Controller"
    elif STXloc<7:
        maxT_loc = maxT_loc + " PA " + str(STXloc+1)
    else:
        maxT_loc = maxT_loc + " Combiners"

    return maxT,maxT_loc,temps

def dataConvert(msg):
    msgStr = str(msg.payload)
    msgClean = [i for i in msgStr[21:-1].split("*")]
    dataSTX = [[],[],[],[]]
    for trs,i in zip(msgClean,[0,1,2,3]) :
        dataSTX[i]= [int(i) for i in trs[1:-1].split(",")]
    # Data to database
    insert(msgStr[2:21],dataSTX)
    # Data to send by socket
    id_STX = dataSTX[0][0] // 4
    status = ''.join([msgClean[i][3] for i in [0,1,2,3]])
    powers = [dataSTX[0][34],dataSTX[0][36],dataSTX[2][32],dataSTX[2][34]]
    tmax,index,tempData = maxTemperature(dataSTX)
    #Json to send
    data = {'time':msgStr[2:21],'num':id_STX,'pow':powers,'tmax':[str(tmax),index],'status':status}
    data_temp = {'time':msgStr[2:21],'temp':tempData}
    return data, data_temp

def GetTemperatures(data):
    np_data = [np.array(i) for i in data]
    temps = [i[i<40] for i in np_data]
    return [i[i>15].tolist() for i in temps]

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
    #    print('Connected successfullyasdss')
       mqtt_client.subscribe("atrad/test4")
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    print('Received message on topic: {} with payload: {}'.format(msg.topic,msg.payload), flush=True)
    mainData, tempData = dataConvert(msg)
    # print("Recibi : {}".format(msg.payload),flush=True)
    #socket fot general data 
    sio.emit('test',data = mainData)
    print(mainData)
    #socket for temperature details 
    sio.emit('temptx'+str(mainData['num'] + 1),data = tempData)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set( '','')
client.connect(
    host=os.environ.get('MQTT_SERVER', '10.10.10.200'),
    port=int(settings.os.environ.get('MQTT_PORT', 1883)),
    keepalive=int(os.environ.get('MQTT_KEEPALIVE', 60))
)