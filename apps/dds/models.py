from django.db import models
from apps.main.models import Configuration
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from devices.dds import api, data

ENABLE_TYPE = (
               (False, 'Disabled'),
               (True, 'Enabled'),
               )
MOD_TYPES = (
                (0, 'Single Tone'),
                (1, 'FSK'),
                (2, 'Ramped FSK'),
                (3, 'Chirp'),
                (4, 'BPSK'),
            )

class DDSConfiguration(Configuration):

    DDS_NBITS = 48

    clock = models.FloatField(verbose_name='Clock In (MHz)',validators=[MinValueValidator(5), MaxValueValidator(75)], null=True, default=60)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=4)

    frequencyA_Mhz = models.DecimalField(verbose_name='Frequency A (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, null=True, default=49.9200)
    frequencyA = models.BigIntegerField(verbose_name='Frequency A (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)

    frequencyB_Mhz = models.DecimalField(verbose_name='Frequency B (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    frequencyB = models.BigIntegerField(verbose_name='Frequency B (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)

    phaseA_degrees = models.FloatField(verbose_name='Phase A (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], default=0)

    phaseB_degrees = models.FloatField(verbose_name='Phase B (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], blank=True, null=True)

    modulation = models.PositiveIntegerField(verbose_name='Modulation Type', choices = MOD_TYPES, default = 0)

    amplitude_enabled = models.BooleanField(verbose_name='Amplitude Control', choices=ENABLE_TYPE, default=False)

    amplitudeI = models.PositiveIntegerField(verbose_name='Amplitude CH1',validators=[MinValueValidator(0), MaxValueValidator(2**12-1)], blank=True, null=True)
    amplitudeQ = models.PositiveIntegerField(verbose_name='Amplitude CH2',validators=[MinValueValidator(0), MaxValueValidator(2**12-1)], blank=True, null=True)


    def get_nbits(self):

        return self.DDS_NBITS

    def clean(self):

        if self.modulation in [1,2,3]:
            if self.frequencyB is None or self.frequencyB_Mhz is None:
                raise ValidationError({
                    'frequencyB': 'Frequency modulation has to be defined when FSK or Chirp modulation is selected'
                })

        if self.modulation in [4,]:
            if self.phaseB_degrees is None:
                raise ValidationError({
                    'phaseB': 'Phase modulation has to be defined when BPSK modulation is selected'
                })

        self.frequencyA_Mhz = data.binary_to_freq(self.frequencyA, self.clock*self.multiplier)
        self.frequencyB_Mhz = data.binary_to_freq(self.frequencyB, self.clock*self.multiplier)

    def verify_frequencies(self):

        return True

    def parms_to_dict(self):

        parameters = {}

        parameters['device_id'] = self.device.id

        parameters['clock'] = float(self.clock)
        parameters['multiplier'] = int(self.multiplier)

        parameters['frequencyA'] = int(self.frequencyA)
        parameters['frequencyA_Mhz'] = float(self.frequencyA_Mhz)

        parameters['phaseA'] = data.phase_to_binary(self.phaseA_degrees)
        parameters['phaseA_degrees'] = float(self.phaseA_degrees)

        parameters['modulation'] = int(self.modulation)
        parameters['amplitude_enabled'] = bool(self.amplitude_enabled)

        if self.frequencyB:
            parameters['frequencyB'] = int(self.frequencyB)
            parameters['frequencyB_Mhz'] = float(self.frequencyB_Mhz)
        else:
            parameters['frequencyB'] = 0
            parameters['frequencyB_Mhz'] = 0

        if self.phaseB_degrees:
            parameters['phaseB_degrees'] = float(self.phaseB_degrees)
            parameters['phaseB'] = data.phase_to_binary(self.phaseB_degrees)
        else:
            parameters['phaseB_degrees'] = 0
            parameters['phaseB'] = 0

        if self.amplitudeI:
            parameters['amplitudeI'] = int(self.amplitudeI)
        else:
            parameters['amplitudeI'] = 0

        if self.amplitudeQ:
            parameters['amplitudeQ'] = int(self.amplitudeQ)
        else:
            parameters['amplitudeQ'] = 0

        return parameters

    def parms_to_text(self):

        my_dict = self.parms_to_dict()

        text = data.dict_to_text(my_dict)

        return text

    def dict_to_parms(self, parameters):

        self.clock = parameters['clock']
        self.multiplier = parameters['multiplier']
        self.frequencyA = parameters['frequencyA']
        self.frequencyB = parameters['frequencyB']
        self.frequencyA_Mhz = parameters['frequencyA_Mhz']
        self.frequencyB_Mhz = parameters['frequencyB_Mhz']
        self.phaseA_degrees = parameters['phaseA_degrees']
        self.phaseB_degrees = parameters['phaseB_degrees']
        self.modulation = parameters['modulation']
        self.amplitude_enabled = parameters['amplitude_enabled']

    def import_from_file(self, fp):

        import os, json

        parms = {}

        path, ext = os.path.splitext(fp.name)

        if ext == '.json':
            parms = json.load(fp)

        if ext == '.dds':
            lines = fp.readlines()
            parms = data.text_to_dict(lines)

        return parms

    def status_device(self):

        try:
            answer = api.status(ip = self.device.ip_address,
                                port = self.device.port_address)
            status = answer[0]
            if status=='0':                
                self.device.status = 1
            else:
                self.device.status = status
            self.message = answer[2:]
            self.device.save()
        except Exception as e:
            self.message = str(e) 
            self.device.status = 0
            self.device.save()
            return False
        
        return True

    def reset_device(self):

        answer = api.reset(ip = self.device.ip_address,
                           port = self.device.port_address)

        if answer[0] != "1":
            self.message = answer[0:]
            return 0

        self.message = answer[2:]
        return 1

    def stop_device(self):

        try:
            answer = api.disable_rf(ip = self.device.ip_address,
                                    port = self.device.port_address)
            if answer[0] == '1':
                self.message = answer[2:]
                self.device.status = 2                
            else:
                self.message = self.message = answer[2:]
                self.device.status = 1
                self.device.save()
                return False
        except Exception as e:
            self.message = str(e)
            return False

        self.device.save()
        return True

    def start_device(self):

        try:
            answer = api.enable_rf(ip = self.device.ip_address,
                                    port = self.device.port_address)
            if answer[0] == '1':
                self.message = 'DDS - RF Enable'
                self.device.status = 3                
            else:
                self.message = self.message = answer[2:]
                self.device.status = 1
                self.device.save()
                return False
        except Exception as e:
            self.message = str(e)
            return False

        self.device.save()
        return True

    def read_device(self):

        parms = api.read_config(ip = self.device.ip_address,
                                port = self.device.port_address)
        if not parms:
            self.message = "Could not read DDS parameters from this device"
            return parms

        self.message = ""
        return parms


    def write_device(self):

        try:
            answer = api.write_config(ip = self.device.ip_address,
                                      port = self.device.port_address,
                                      parms = self.parms_to_dict())
            if answer[0] == '1':
                self.message = answer[2:]
                self.device.status = 3
            else:
                self.message = answer[2:]            
                self.device.status = 1
                self.device.save()
                return False
        except Exception as e:
            self.message = str(e)
            return False

        self.device.save()
        return True
    
    class Meta:
        db_table = 'dds_configurations'
