# Generated by Django 5.1.3 on 2024-11-12 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_sensordata_sensor_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensordata',
            options={'ordering': ['-sensor_timestamp']},
        ),
    ]
