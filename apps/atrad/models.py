from django.db import models
from apps.main.models import Configuration
from apps.main.utils import Params
from django.core.validators import MinValueValidator, MaxValueValidator

from .files import read_json_file
import requests

class ATRADData(models.Model):
    datetime = models.DateTimeField()

    nstx = models.SmallIntegerField()

    status_1 = models.SmallIntegerField()
    temp_cll_1 = models.SmallIntegerField()
    nboards_1 = models.SmallIntegerField()
    tempdvr_1 = models.SmallIntegerField()
    potincdvr_1 = models.SmallIntegerField()
    potretdvr_1 = models.SmallIntegerField()
    
    temp1_1 = models.SmallIntegerField()
    potinc1_1 = models.SmallIntegerField()
    potret1_1 = models.SmallIntegerField()
    temp2_1 = models.SmallIntegerField()
    potinc2_1 = models.SmallIntegerField()
    potret2_1 = models.SmallIntegerField()
    temp3_1 = models.SmallIntegerField()
    potinc3_1 = models.SmallIntegerField()
    potret3_1 = models.SmallIntegerField()
    temp4_1 = models.SmallIntegerField()
    potinc4_1 = models.SmallIntegerField()
    potret4_1 = models.SmallIntegerField()
    temp5_1 = models.SmallIntegerField()
    potinc5_1 = models.SmallIntegerField()
    potret5_1 = models.SmallIntegerField()
    temp6_1 = models.SmallIntegerField()
    potinc6_1 = models.SmallIntegerField()
    potret6_1 = models.SmallIntegerField()

    status_2 = models.SmallIntegerField()
    temp_cll_2 = models.SmallIntegerField()
    nboards_2 = models.SmallIntegerField()
    tempdvr_2 = models.SmallIntegerField()
    potincdvr_2 = models.SmallIntegerField()
    potretdvr_2 = models.SmallIntegerField()

    temp1_2 = models.SmallIntegerField()
    potinc1_2 = models.SmallIntegerField()
    potret1_2 = models.SmallIntegerField()
    temp2_2 = models.SmallIntegerField()
    potinc2_2 = models.SmallIntegerField()
    potret2_2 = models.SmallIntegerField()
    temp3_2 = models.SmallIntegerField()
    potinc3_2 = models.SmallIntegerField()
    potret3_2 = models.SmallIntegerField()
    temp4_2 = models.SmallIntegerField()
    potinc4_2 = models.SmallIntegerField()
    potret4_2 = models.SmallIntegerField()
    temp5_2 = models.SmallIntegerField()
    potinc5_2 = models.SmallIntegerField()
    potret5_2 = models.SmallIntegerField()
    temp6_2 = models.SmallIntegerField()
    potinc6_2 = models.SmallIntegerField()
    potret6_2 = models.SmallIntegerField()

    status_3 = models.SmallIntegerField()
    temp_cll_3 = models.SmallIntegerField()
    nboards_3 = models.SmallIntegerField()
    tempdvr_3 = models.SmallIntegerField()
    potincdvr_3 = models.SmallIntegerField()
    potretdvr_3 = models.SmallIntegerField()

    temp1_3 = models.SmallIntegerField()
    potinc1_3 = models.SmallIntegerField()
    potret1_3 = models.SmallIntegerField()
    temp2_3 = models.SmallIntegerField()
    potinc2_3 = models.SmallIntegerField()
    potret2_3 = models.SmallIntegerField()
    temp3_3 = models.SmallIntegerField()
    potinc3_3 = models.SmallIntegerField()
    potret3_3 = models.SmallIntegerField()
    temp4_3 = models.SmallIntegerField()
    potinc4_3 = models.SmallIntegerField()
    potret4_3 = models.SmallIntegerField()
    temp5_3 = models.SmallIntegerField()
    potinc5_3 = models.SmallIntegerField()
    potret5_3 = models.SmallIntegerField()
    temp6_3 = models.SmallIntegerField()
    potinc6_3 = models.SmallIntegerField()
    potret6_3 = models.SmallIntegerField()

    status_4 = models.SmallIntegerField()
    temp_cll_4 = models.SmallIntegerField()
    nboards_4 = models.SmallIntegerField()
    tempdvr_4 = models.SmallIntegerField()
    potincdvr_4 = models.SmallIntegerField()
    potretdvr_4 = models.SmallIntegerField()

    temp1_4 = models.SmallIntegerField()
    potinc1_4 = models.SmallIntegerField()
    potret1_4 = models.SmallIntegerField()
    temp2_4 = models.SmallIntegerField()
    potinc2_4 = models.SmallIntegerField()
    potret2_4 = models.SmallIntegerField()
    temp3_4 = models.SmallIntegerField()
    potinc3_4 = models.SmallIntegerField()
    potret3_4 = models.SmallIntegerField()
    temp4_4 = models.SmallIntegerField()
    potinc4_4 = models.SmallIntegerField()
    potret4_4 = models.SmallIntegerField()
    temp5_4 = models.SmallIntegerField()
    potinc5_4 = models.SmallIntegerField()
    potret5_4 = models.SmallIntegerField()
    temp6_4 = models.SmallIntegerField()
    potinc6_4 = models.SmallIntegerField()
    potret6_4 = models.SmallIntegerField()

    class Meta:
        db_table = 'atrad_datas'
    
    def __unicode__(self):
        return u'%s' % (self.name)

class ATRADConfiguration(Configuration):

    topic = models.PositiveIntegerField(verbose_name='Topic',validators=[MaxValueValidator(10)], default = 0)

    def status_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        route = "http://" + str(ip) + ":" + str(port) + "/status/"
        try:
            r = requests.get(route, timeout=0.7)
        except Exception as e:
            self.device.status = 0
            self.device.save()
            self.message = 'Could not read TX status: ' + str(e)
            return False

        response = r.json()
        self.device.status = response['status']
        self.message = response['message']
        self.device.save()

        if response['components_status']==0:
            return False

        return True


    def start_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        #---Device must be configured
        if not self.device.status == 2:
            self.message = 'TX Device must be configured.'
            return False
        #---Frequencies from form
        post_data = self.parms_to_dict()
        route = "http://" + str(ip) + ":" + str(port) + "/write/"

        try:
            r = requests.post(route, post_data, timeout=0.7)
        except Exception as e:
            self.message = "Could not start TX device. "+str(e)
            return False

        response = r.json()
        if response['status']==1:
            self.device.status = 1
            self.device.save()
            self.message = response['message']
            return False

        self.device.status = response['status']
        self.device.save()
        self.message = response['message']

        return True


    def stop_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        if self.device.status == 2: #Configured
            self.message = 'TX device is already stopped.'
            return False

        post_data = {"topic":0}
        route = "http://" + str(ip) + ":" + str(port) + "/write/"

        try:
            r = requests.post(route, post_data, timeout=0.7)
        except Exception as e:
            self.message = "Could not write TX parameters. "+str(e)
            self.device.status = 0
            self.device.save()
            return False

        response = r.json()
        status = response['status']
        if status == 1:
            self.device.status = status
            self.device.save()
            self.message = 'Could not stop TX device.'
            return False

        self.message = 'TX device has been stopped successfully.'
        self.device.status = 2
        self.device.save()

        return True


    def read_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        route = "http://" + str(ip) + ":" + str(port) + "/read/"
        try:
            frequencies = requests.get(route,timeout=0.7)
        except:
            self.message = "Could not read TX parameters from this device"
            return None

        frequencies = frequencies.json()
        if frequencies:
            frequencies = frequencies.get("Frequencies")
            topic = frequencies.get("topic")

            parms = {'topic': topic}

            self.message = "TX parameters have been successfully read"
            return parms
        else:
            self.message = "Error reading TX parameters"
            return None


    def write_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        #---Frequencies from form
        parms = self.parms_to_dict()['configurations']
        for parm in parms['allIds']:
                byid = parm
        frequencies = parms['byId'][byid]
        post_data = {}
        for data in frequencies:
            if data in ['topic']:
                post_data[data] = frequencies[data]

        route = "http://" + str(ip) + ":" + str(port) + "/write/"
        print (post_data)
        try:
            r = requests.post(route, post_data, timeout=0.7)
        except:
            self.message = "Could not write TX parameters"
            self.device.status = 0
            self.device.save()
            return False

        response = r.json()
        self.message = response['message']
        self.device.status = response['status']
        self.device.save()

        if self.device.status==1:
            return False

        return True


    class Meta:
        db_table = 'atrad_configurations'