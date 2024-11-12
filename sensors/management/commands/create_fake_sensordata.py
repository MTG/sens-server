import random
from datetime import datetime, timedelta
import uuid
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from sensors.models import SensorData
import sys
import pytz


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

class Command(BaseCommand):
    help = 'Create fake SensorData objects for the last 12 hours'

    def handle(self, *args, **kwargs):
        now = make_aware(datetime.now())
        twelve_hours_ago = now - timedelta(hours=12)
        interval = timedelta(minutes=1) / 20  # 20 objects per minute

        # Check for the latest SensorData object
        latest_data = SensorData.objects.filter(sensor_timestamp__gte=twelve_hours_ago).order_by('-sensor_timestamp').first()
        start_time = max(latest_data.sensor_timestamp, twelve_hours_ago) if latest_data else twelve_hours_ago

        # Initial data
        data = {
            'sources': {
                'birds': 0.03,
                'construction': 0.87,
                'dogs': 0.15,
                'human': 0.03,
                'music': 0.12,
                'nature': 0.48,
                'siren': 0.13,
                'vehicles': 0.41
            },
            'pleasantness_inst': -0.15,
            'eventfulness_inst': -0.13,
            'pleasantness_intg': -0.05,
            'eventfulness_intg': -0.10,
            'leq': 72.4
        }

        # Generate fake data
        i = 0
        num_total_minutes = int((now - start_time).total_seconds() / 60)
        num_data_points = num_total_minutes * 20
        while start_time < now:
            start_time += interval

            # Gradually change values
            for key in data['sources']:
                data['sources'][key] += random.uniform(-0.01, 0.01)
                data['sources'][key] = max(0, min(1, data['sources'][key]))  # Keep values between 0 and 1

            data['pleasantness_inst'] += random.uniform(-0.01, 0.01)
            data['eventfulness_inst'] += random.uniform(-0.01, 0.01)
            data['pleasantness_intg'] += random.uniform(-0.01, 0.01)
            data['eventfulness_intg'] += random.uniform(-0.01, 0.01)
            data['leq'] += random.uniform(-0.5, 0.5)

            # Randomly add or remove sources
            #if random.random() < 0.1:  # 10% chance to add/remove a source
            #    if random.random() < 0.5 and len(data['sources']) > 1:
            #        data['sources'].pop(random.choice(list(data['sources'].keys())))
            #    else:
            #        new_source = f'source_{random.randint(1, 100)}'
            #        data['sources'][new_source] = random.uniform(0, 1)

            # Create SensorData object
            SensorData.objects.create(
                uuid=str(uuid.uuid4()),
                sensor_id='fake_sensor',
                sensor_timestamp=start_time,
                data=data
            )

            # Print progress bar
            print_progress_bar(i + 1, num_data_points, prefix='Progress:', suffix='Complete', length=50)
            i += 1

        self.stdout.write(self.style.SUCCESS('Successfully created fake SensorData objects'))