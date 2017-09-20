from django.db import models
from apps.main.models import Configuration
from apps.main.utils import Params
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

    def parms_to_text(self):

        my_dict = self.parms_to_dict()['configurations']['byId'][str(self.id)]

        text = data.dict_to_text(my_dict)

        return text

    def status_device(self):

        try:
            answer = api.status(ip = self.device.ip_address,
                                port = self.device.port_address)
            if 'clock' in answer:
                self.device.status = 1
            else:
                self.device.status = answer[0]
            self.message = 'DDS - {}'.format(answer[2:])
        except Exception as e:
            self.message = str(e)
            self.device.status = 0

        self.device.save()

        if self.device.status in (0, '0'):
            return False
        else:
            return True

    def reset_device(self):

        answer = api.reset(ip = self.device.ip_address,
                           port = self.device.port_address)

        if answer[0] != "1":
            self.message = 'DDS - {}'.format(answer[2:])
            return 0

        self.message = 'DDS - {}'.format(answer[2:])
        return 1

    def stop_device(self):

        try:
            answer = api.disable_rf(ip = self.device.ip_address,
                                    port = self.device.port_address)

            return self.status_device()

        except Exception as e:
            self.message = str(e)
            return False

    def start_device(self):

        try:
            answer = api.enable_rf(ip = self.device.ip_address,
                                    port = self.device.port_address)

            return self.status_device()

        except Exception as e:
            self.message = str(e)
            return False

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
                                      parms = self.parms_to_dict()['configurations']['byId'][str(self.id)])

            return self.status_device()

        except Exception as e:
            self.message = str(e)
            return False

    class Meta:
        db_table = 'dds_configurations'
