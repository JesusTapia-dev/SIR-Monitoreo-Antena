import ast
import json
import requests
import numpy as np
from base64 import b64encode
from struct import pack

from django.urls import reverse
from django.db import models
from apps.main.models import Configuration
from apps.main.utils import Params
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from devices.dds_rest import api, data

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

class DDSRestConfiguration(Configuration):

    DDS_NBITS = 48

    clock      = models.FloatField(verbose_name='Clock In (MHz)',validators=[MinValueValidator(5), MaxValueValidator(75)], null=True, default=60)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=4)

    frequencyA_Mhz = models.DecimalField(verbose_name='Frequency A (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, null=True, default=49.9200)
    frequencyA     = models.BigIntegerField(verbose_name='Frequency A (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)

    frequencyB_Mhz = models.DecimalField(verbose_name='Frequency B (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    frequencyB     = models.BigIntegerField(verbose_name='Frequency B (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)

    delta_frequency_Mhz = models.DecimalField(verbose_name='Delta frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    delta_frequency     = models.BigIntegerField(verbose_name='Delta frequency (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)

    update_clock_Mhz = models.DecimalField(verbose_name='Update clock (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    update_clock     = models.BigIntegerField(verbose_name='Update clock (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**32-1)], blank=True, null=True)

    ramp_rate_clock_Mhz = models.DecimalField(verbose_name='Ramp rate clock (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    ramp_rate_clock     = models.BigIntegerField(verbose_name='Ramp rate clock (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**18-1)], blank=True, null=True)

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

    def parms_to_text(self):

        my_dict = self.parms_to_dict()['configurations']['byId'][str(self.id)]

        text = data.dict_to_text(my_dict)

        return text

    def status_device(self):
        print("Status ")
        try:
            self.device.status = 0
            payload = self.request('status')
            if payload['status']=='generating RF':
                self.device.status = 3
            elif payload['status']=='no generating RF':
                self.device.status = 2
            else:
                self.device.status = 1
                self.device.save()
                self.message = 'DDS REST status: {}'.format(payload['status'])
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            self.device.save()
            self.message = 'DDS REST status: {}'.format(str(e))
            return False

        self.device.save()
        return True

    def reset_device(self):

        try:
            payload = self.request('reset', 'post')
            if payload['reset']=='ok':
                self.message = 'DDS REST restarted OK'
                self.device.status = 2
                self.device.save()
            else:
                self.message = 'DDS REST restart fail'
                self.device.status = 4
                self.device.save()
        except Exception as e:
            self.message = 'DDS REST reset: {}'.format(str(e))
            return False

        return True

    def stop_device(self):

        # Se crea el modo ocupado para una vez inicia el STOP
        self.device.status = 5
        self.device.save()
        # Por si se demora deteniendo, que su estado sea busy

        try:
            payload = self.request('stop', 'post',data=json.dumps({'_rf_enable':0}))
            self.message = 'DDS REST: {}'.format(payload['stop'])
            if payload['stop']=='ok':
                self.device.status = 2
                self.device.save()
            else:
                self.device.status = 4
                self.device.save()
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = 'DDS REST stop: {}'.format(str(e))
            self.device.save()
            return False

        return True

    def start_device(self):

        try:
            payload = self.request('start', 'post',data=json.dumps({'_rf_enable':1}))
            self.message = 'DDS REST start: {}'.format(payload['start'])
            if payload['start']=='ok':
                self.device.status = 3
                self.device.save()
            else:
                self.device.status = 2
                self.device.save()                
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = 'DDS REST start: {}'.format(str(e))
            self.device.save()
            return False

        return True

    def read_device(self):

        parms = self.request('read')
        print(parms)
        if not parms:
            self.message = "Could not read DDS REST parameters from this device"
            return parms

        self.message = ""
        return parms

    def arma_control(self,l_clock,l_multiplier,l_modulation):
        sysclock  = l_clock*l_multiplier
        pll_range = 0
        if(sysclock>=200):
             pll_range = 1
        l_control = ((l_modulation<<9)+(pll_range<<22)+(l_multiplier<<16)).to_bytes(4,'little') 
        return l_control

    def conv_phase(self,l_phase):
        
        l_phase_2B = int((l_phase*(2**14)/360)).to_bytes(2,'little') 
        return l_phase_2B

    def arma_data_write(self):
        #clock = RCClock.objects.get(rc_configuration=self)
        clock = self.clock
        print(clock)
        multiplier = self.multiplier
        print(multiplier)
        frequencyA_Mhz = self.frequencyA_Mhz
        print(frequencyA_Mhz)
        frequencyA = self.frequencyA
        print(frequencyA)
        frequencyB_Mhz = self.frequencyB_Mhz
        print(frequencyB_Mhz)
        frequencyB = self.frequencyB
        print(frequencyB)
        phaseA_degrees = self.phaseA_degrees or 0
        print(phaseA_degrees)
        phaseB_degrees = self.phaseB_degrees or 0
        print(phaseB_degrees)
        modulation = self.modulation or 0
        print(modulation)
        amplitude_enabled = self.amplitude_enabled or 0
        print(amplitude_enabled)
        amplitudeI = self.amplitudeI or 0
        print(amplitudeI)
        amplitudeQ = self.amplitudeQ or 0
        print(amplitudeQ)
        delta_frequency = self.delta_frequency or 0
        print(delta_frequency)
        update_clock = self.update_clock or 0
        print(update_clock)
        ramp_rate_clock = self.ramp_rate_clock or 0
        print(ramp_rate_clock)
        osrr = 0
        qdac = 0
        control = self.arma_control(clock,multiplier,modulation)
        phase1  = self.conv_phase(phaseA_degrees)
        phase2  = self.conv_phase(phaseB_degrees)

        cadena_json = {'clock': (b64encode(pack('<f',clock))).decode("UTF-8"),\
        'multiplier': (b64encode(pack('<B',multiplier))).decode("UTF-8"),\
        'frequencyA': (b64encode((frequencyA).to_bytes(6,'little'))).decode("UTF-8"),\
        'frequencyB': (b64encode((frequencyB).to_bytes(6,'little'))).decode("UTF-8"),\
        'delta_frequency': (b64encode((delta_frequency).to_bytes(6,'little'))).decode("UTF-8"),\
        'update_clock': (b64encode((update_clock).to_bytes(4,'little'))).decode("UTF-8"),\
        'ramp_rate_clock': (b64encode((ramp_rate_clock).to_bytes(3,'little'))).decode("UTF-8"),\
        'control': (b64encode(control)).decode("UTF-8"),\
        'amplitudeI': (b64encode((amplitudeI).to_bytes(2,'little'))).decode("UTF-8"),\
        'amplitudeQ': (b64encode((amplitudeQ).to_bytes(2,'little'))).decode("UTF-8"),\
        '_phase1': (b64encode((phase1))).decode("UTF-8"),\
        '_phase2': (b64encode((phase2))).decode("UTF-8"),\
        'osrr': (b64encode((osrr).to_bytes(1,'little'))).decode("UTF-8"),\
        'qdac': (b64encode((qdac).to_bytes(2,'little'))).decode("UTF-8")                                
        }
        return cadena_json

    def write_device(self, raw=False):
        print("Ingreso a write")
        try:

            if not raw:
                data = self.arma_data_write()
                print(data)
                payload = self.request('write', 'post', data=json.dumps(data))
                print(payload)
                if payload['write'] == 'ok':
                    self.device.status = 3
                    self.device.save()
                    self.message = 'DDS Rest write configured and started'
                else:
                    self.message = payload['programming']
                    if payload['programming'] == 'fail':
                        self.message = 'DDS Rest write: error programming DDS chip'
            if raw:
                return b64encode(data)


        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = 'DDS Rest write: {}'.format(str(e))
            self.device.save()
            return False

        return True

    def request(self, cmd, method='get', **kwargs):
        print("Ingreso a request")
        req = getattr(requests, method)(self.device.url(cmd), **kwargs)
        payload = req.json()

        return payload

    class Meta:
        db_table = 'ddsrest_configurations'
