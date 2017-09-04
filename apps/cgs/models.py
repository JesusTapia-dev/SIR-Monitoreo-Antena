from django.db import models
from apps.main.models import Configuration
from apps.main.utils import Params
from django.core.validators import MinValueValidator, MaxValueValidator

from .files import read_json_file
import requests
# Create your models here. validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)]

class CGSConfiguration(Configuration):

    freq0 = models.PositiveIntegerField(verbose_name='Frequency 0 (Hz)',validators=[MaxValueValidator(450e6)], default = 60)
    freq1 = models.PositiveIntegerField(verbose_name='Frequency 1 (Hz)',validators=[MaxValueValidator(450e6)], default = 60)
    freq2 = models.PositiveIntegerField(verbose_name='Frequency 2 (Hz)',validators=[MaxValueValidator(450e6)], default = 60)
    freq3 = models.PositiveIntegerField(verbose_name='Frequency 3 (Hz)',validators=[MaxValueValidator(450e6)], default = 60)

    def verify_frequencies(self):

        return True


    def status_device(self):

        ip=self.device.ip_address
        port=self.device.port_address

        route = "http://" + str(ip) + ":" + str(port) + "/status/"
        try:
            r = requests.get(route, timeout=0.7)
        except Exception as e:
            self.device.status = 0
            self.device.save()
            self.message = 'Could not read CGS status: ' + str(e)
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
            self.message = 'CGS Device must be configured.'
            return False
        #---Frequencies from form
        post_data = self.parms_to_dict()
        route = "http://" + str(ip) + ":" + str(port) + "/write/"

        try:
            r = requests.post(route, post_data, timeout=0.7)
        except Exception as e:
            self.message = "Could not start CGS device. "+str(e)
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
            self.message = 'CGS device is already stopped.'
            return False

        post_data = {"freq0":0, "freq1":0, "freq2":0, "freq3":0}
        route = "http://" + str(ip) + ":" + str(port) + "/write/"

        try:
            r = requests.post(route, post_data, timeout=0.7)
        except Exception as e:
            self.message = "Could not write CGS parameters. "+str(e)
            self.device.status = 0
            self.device.save()
            return False

        response = r.json()
        status = response['status']
        if status == 1:
            self.device.status = status
            self.device.save()
            self.message = 'Could not stop CGS device.'
            return False

        self.message = 'CGS device has been stopped successfully.'
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
            self.message = "Could not read CGS parameters from this device"
            return None

        frequencies = frequencies.json()
        if frequencies:
            frequencies = frequencies.get("Frequencies")
            freq0 = frequencies.get("freq0")
            freq1 = frequencies.get("freq1")
            freq2 = frequencies.get("freq2")
            freq3 = frequencies.get("freq3")

            parms = {'freq0': freq0,
                 'freq1': freq1,
                 'freq2': freq2,
                 'freq3': freq3}

            self.message = "CGS parameters have been successfully read"
            return parms
        else:
            self.message = "Error reading CGS parameters"
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
            if data in ['freq0','freq1','freq2','freq3']:
                post_data[data] = frequencies[data]

        route = "http://" + str(ip) + ":" + str(port) + "/write/"
        print post_data
        try:
            r = requests.post(route, post_data, timeout=0.7)
        except:
            self.message = "Could not write CGS parameters"
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
        db_table = 'cgs_configurations'
