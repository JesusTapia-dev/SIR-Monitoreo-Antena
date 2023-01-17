# Generated by Django 2.2.1 on 2023-01-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ABSActive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'abs_absactive',
            },
        ),
        migrations.CreateModel(
            name='ABSBeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Beam', max_length=60)),
                ('antenna', models.CharField(default='{"antenna_up": [[0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0], [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0], [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0], [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0]], "antenna_down": [[0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 3.0, 3.0, 3.0, 3.0], [0.5, 0.5, 0.5, 0.5, 3.0, 3.0, 3.0, 3.0], [0.5, 0.5, 0.5, 0.5, 3.0, 3.0, 3.0, 3.0], [0.5, 0.5, 0.5, 0.5, 3.0, 3.0, 3.0, 3.0]]}', max_length=1000, verbose_name='Antenna')),
                ('tx', models.CharField(default='{"up": [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1]], "down": [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1]]}', max_length=1000, verbose_name='Tx')),
                ('rx', models.CharField(default='{"up": [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1]], "down": [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1]]}', max_length=1000, verbose_name='Rx')),
                ('s_time', models.TimeField(default='00:00:00', verbose_name='Star Time')),
                ('e_time', models.TimeField(default='23:59:59', verbose_name='End Time')),
                ('ues', models.CharField(default='{"up": [0.533333, 0.0, 1.06667, 0.0], "down": [0.533333, 0.0, 1.06667, 0.0]}', max_length=100, verbose_name='Ues')),
                ('only_rx', models.CharField(default='{"up": false, "down": false}', max_length=40, verbose_name='Only RX')),
            ],
            options={
                'db_table': 'abs_beams',
            },
        ),
    ]
