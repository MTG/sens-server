from django.urls import path
from . import views

urlpatterns = [
    # Api views
    path('api/sensor-data/', views.post_sensor_data_point, name='post_sensor_data_point'),
    path('api/sensor-data/sensor-ids/', views.list_sensor_ids, name='list_sensor_ids'),
    path('api/sensor-data/time-range/', views.get_sensor_data_by_time_range, name='get_sensor_data_by_time_range'),
    path('api/sensor-data/<str:sensor_id>/', views.get_sensor_data, name='get_sensor_data'),
    path('api/sensor-data/<str:sensor_id>/time-range/', views.get_sensor_data_by_sensor_and_time_range, name='get_sensor_data_by_sensor_and_time_range'),
    
    # Web views
    path('sensor/<str:sensor_id>/', views.sensor_data_view, name='sensor_data_view'),
    path('multiple_sensors/', views.multiple_sensor_data_view, name='multiple_sensor_data_view'),
    
    # Frontpage
    path('', views.frontpage, name='frontpage'),
]