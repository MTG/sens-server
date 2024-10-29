from django.db import models


class SensorData(models.Model):
    sensor_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    data = models.JSONField()  # Stores arbitrary JSON data

    def __str__(self):
        return f"Sensor {self.sensor_id} at {self.timestamp}"