from rest_framework import serializers
from .models import SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['uuid', 'sensor_id', 'timestamp', 'sensor_timestamp', 'location', 'data']