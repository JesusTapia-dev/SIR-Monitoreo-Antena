import paho.mqtt.client as mqtt
from radarsys import settings
from radarsys.socketconfig import sio as sio
import numpy as np
import psycopg2
import os

def insert(time,data):
    sql = """INSERT INTO atrad_datas(
        datetime,nstx,status_1,temp_cll_1,nboards_1,tempdvr_1,potincdvr_1,potretdvr_1,
        temp1_1,potinc1_1,potret1_1,temp2_1,potinc2_1,potret2_1,temp3_1,potinc3_1,potret3_1,
        temp4_1,potinc4_1,potret4_1,temp5_1,potinc5_1,potret5_1,temp6_1,potinc6_1,potret6_1,
        status_2,temp_cll_2,nboards_2,tempdvr_2,potincdvr_2,potretdvr_2,
        temp1_2,potinc1_2,potret1_2,temp2_2,potinc2_2,potret2_2,temp3_2,potinc3_2,potret3_2,
        temp4_2,potinc4_2,potret4_2,temp5_2,potinc5_2,potret5_2,temp6_2,potinc6_2,potret6_2,
        status_3,temp_cll_3,nboards_3,tempdvr_3,potincdvr_3,potretdvr_3,
        temp1_3,potinc1_3,potret1_3,temp2_3,potinc2_3,potret2_3,temp3_3,potinc3_3,potret3_3,
        temp4_3,potinc4_3,potret4_3,temp5_3,potinc5_3,potret5_3,temp6_3,potinc6_3,potret6_3,
        status_4,temp_cll_4,nboards_4,tempdvr_4,potincdvr_4,potretdvr_4,
        temp1_4,potinc1_4,potret1_4,temp2_4,potinc2_4,potret2_4,temp3_4,potinc3_4,potret3_4,
        temp4_4,potinc4_4,potret4_4,temp5_4,potinc5_4,potret5_4,temp6_4,potinc6_4,potret6_4,
        combiner1,combiner2,combiner3,combiner4)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s);"""
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(database="radarsys", user='docker', password='docker', host='radarsys-postgres', port= '5432')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        #data_tuple = [tuple(i[:]) for i in a]
        values = (time,) + tuple(data[0][:25])+tuple(data[1][1:25])+tuple(data[2][1:25])+tuple(data[3][1:25]) + tuple(data[0][29:31]) +tuple(data[2][27:29])
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
    elif STXloc == 1:
        maxT_loc = maxT_loc + " Driver"
    elif STXloc<8:
        maxT_loc = maxT_loc + " PA " + str(STXloc-1)
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
    powers = [dataSTX[0][34],dataSTX[0][36],dataSTX[2][32],dataSTX[2][34],0,0,0,0]
    # alerta
    for i in range(4):
        if powers[i] < 10000 and status == '1111':
            power[4+i] = 1

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
       mqtt_client.subscribe(os.environ.get('MQTT_TOPIC_ATRAD_RECIEVE', 'atrad/test4'))
    #    print("Exito")
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    print('Received message on topic: {} with payload: {}'.format(msg.topic,msg.payload), flush=True)
    mainData, tempData = dataConvert(msg)
    sio.emit('test',data = mainData)
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
