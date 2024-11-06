from django.db import models


class SensorData(models.Model):
    uuid = models.CharField(max_length=100)
    sensor_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_timestamp = models.DateTimeField()
    location = models.CharField(max_length=255)
    data = models.JSONField()  # Stores arbitrary JSON data

    def __str__(self):
        return f"Sensor {self.sensor_id} at {self.timestamp}"
    
    class Meta:
        ordering = ['-sensor_timestamp']