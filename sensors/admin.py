from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('sensor_id', 'sensor_timestamp', 'timestamp', 'location', 'data', 'uuid')

    # Add filters to the right side of the admin
    list_filter = ('sensor_id', 'sensor_timestamp', 'timestamp', 'location')

    # Add search functionality for sensor_id and location fields
    search_fields = ('sensor_id', 'location', 'uuid')

    # Add ordering
    ordering = ('-sensor_timestamp',)