# Generated by Django 2.2.1 on 2023-01-17 09:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JARSFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60, unique=True, verbose_name='Name')),
                ('clock', models.FloatField(default=60, null=True, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(75)], verbose_name='Clock In (MHz)')),
                ('multiplier', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='Multiplier')),
                ('frequency', models.FloatField(default=49.92, null=True, validators=[django.core.validators.MaxValueValidator(150)], verbose_name='Frequency (MHz)')),
                ('f_decimal', models.BigIntegerField(default=721554505, null=True, validators=[django.core.validators.MinValueValidator(-9223372036854775808), django.core.validators.MaxValueValidator(4294967295)], verbose_name='Frequency (Decimal)')),
                ('cic_2', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(100)], verbose_name='CIC2')),
                ('scale_cic_2', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)], verbose_name='Scale CIC2')),
                ('cic_5', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='CIC5')),
                ('scale_cic_5', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Scale CIC5')),
                ('fir', models.PositiveIntegerField(default=6, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='FIR')),
                ('scale_fir', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)], verbose_name='Scale FIR')),
                ('number_taps', models.PositiveIntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(256)], verbose_name='Number of taps')),
                ('taps', models.CharField(default='0', max_length=1600, verbose_name='Taps')),
            ],
            options={
                'db_table': 'jars_filters',
            },
        ),
        migrations.CreateModel(
            name='JARSConfiguration',
            fields=[
                ('configuration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Configuration')),
                ('exp_type', models.PositiveIntegerField(choices=[(0, 'RAW_DATA'), (1, 'PDATA')], default=0, verbose_name='Experiment Type')),
                ('cards_number', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Cards')),
                ('channels_number', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)], verbose_name='Number of Channels')),
                ('channels', models.CharField(default='1,2,3,4,5', max_length=15, verbose_name='Channels')),
                ('data_type', models.PositiveIntegerField(choices=[(0, 'SHORT'), (1, 'FLOAT')], default=0, verbose_name='Data Type')),
                ('raw_data_blocks', models.PositiveIntegerField(default=60, validators=[django.core.validators.MaxValueValidator(5000)], verbose_name='Raw Data Blocks')),
                ('profiles_block', models.PositiveIntegerField(default=400, verbose_name='Profiles Per Block')),
                ('acq_profiles', models.PositiveIntegerField(default=400, verbose_name='Acquired Profiles')),
                ('ftp_interval', models.PositiveIntegerField(default=60, verbose_name='FTP Interval')),
                ('fftpoints', models.PositiveIntegerField(default=16, verbose_name='FFT Points')),
                ('cohe_integr_str', models.PositiveIntegerField(default=30, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Coh. Int. Stride')),
                ('cohe_integr', models.PositiveIntegerField(default=30, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Coherent Integrations')),
                ('incohe_integr', models.PositiveIntegerField(default=30, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Incoherent Integrations')),
                ('decode_data', models.PositiveIntegerField(choices=[(0, 'None'), (1, 'TimeDomain'), (2, 'FreqDomain'), (3, 'InvFreqDomain')], default=0, verbose_name='Decode Data')),
                ('post_coh_int', models.BooleanField(default=False, verbose_name='Post Coherent Integration')),
                ('spectral_number', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='# Spectral Combinations')),
                ('spectral', models.CharField(default='[0, 0],', max_length=5000, verbose_name='Combinations')),
                ('create_directory', models.BooleanField(default=True, verbose_name='Create Directory Per Day')),
                ('include_expname', models.BooleanField(default=False, verbose_name='Experiment Name in Directory')),
                ('save_ch_dc', models.BooleanField(default=True, verbose_name='Save Channels DC')),
                ('save_data', models.BooleanField(default=True, verbose_name='Save Data')),
                ('filter_parms', models.CharField(default='{"id":1, "clock": 60, "multiplier": 5, "frequency": 49.92, "f_decimal":\t721554506, "fir": 2, "cic_2": 12, "cic_5": 25}', max_length=10000)),
                ('filter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jars.JARSFilter', verbose_name='Filter')),
            ],
            options={
                'db_table': 'jars_configurations',
            },
            bases=('main.configuration',),
        ),
    ]
