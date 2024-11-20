import os 
import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import SensorData
from .serializers import SensorDataSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Q

@api_view(['POST'])
def post_sensor_data_point(request):
    if request.method == 'POST':
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_sensor_data(request, sensor_id):
    try:
        sensor_data = SensorData.objects.filter(sensor_id=sensor_id)
    except SensorData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SensorDataSerializer(sensor_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_sensor_data_by_time_range(request):
    # Get start_date and end_date from query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"error": "Please provide both start_date and end_date in 'YYYY-MM-DD' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Parse the dates
    try:
        start_datetime = parse_datetime(start_date)
        end_datetime = parse_datetime(end_date)
    except ValueError:
        return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    if start_datetime is None or end_datetime is None:
        return Response({"error": "Invalid date format or missing time. Use 'YYYY-MM-DDTHH:MM:SSZ' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Filter the data based on the time range
    sensor_data = SensorData.objects.filter(Q(sensor_timestamp__gte=start_datetime) & Q(sensor_timestamp__lte=end_datetime))

    # Serialize and return the filtered data
    serializer = SensorDataSerializer(sensor_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_sensor_data_by_sensor_and_time_range(request, sensor_id):
    # Get start_date and end_date from query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"error": "Please provide both start_date and end_date in 'YYYY-MM-DD' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Parse the dates
    try:
        start_datetime = parse_datetime(start_date)
        end_datetime = parse_datetime(end_date)
    except ValueError:
        return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    if start_datetime is None or end_datetime is None:
        return Response({"error": "Invalid date format or missing time. Use 'YYYY-MM-DDTHH:MM:SSZ' format."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Filter the data based on sensor_id and time range
    sensor_data = SensorData.objects.filter(
        sensor_id=sensor_id,
        sensor_timestamp__gte=start_datetime,
        sensor_timestamp__lte=end_datetime
    )[0:1000]  # Limit the number of results to 1000

    # Serialize and return the filtered data
    serializer = SensorDataSerializer(sensor_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_sensor_ids(request):
    # Retrieve distinct sensor IDs from the SensorData model
    sensor_ids = sorted(list(set(SensorData.objects.values_list('sensor_id', flat=True))))

    # Return the list of sensor IDs
    return Response(sensor_ids, status=status.HTTP_200_OK)


def _process_sensor_data_form(request):
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)
    if start_time == '':
        start_time = None
    if end_time == '':
        end_time = None
    if start_time is None or end_time is None:  # If only one is provided, set both to None
        start_time = None
        end_time = None
    time_range = request.GET.get('time_range', None)
    real_time = request.GET.get('real_time', False)
    time_range_options = [
        (1, 'Last Minute'),
        (10, 'Last 10 Minutes'),
        (30, 'Last 30 Minutes'),
        (60, 'Last Hour'),
        (720, 'Last 12 Hours'),
        (1440, 'Last 24 Hours')
    ]
    default_time_range = 10

    if start_time is None and end_time is None and time_range is None:
        time_range = default_time_range
    elif start_time is not None and end_time is not None:
        time_range = int(time_range)
        try:
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            start_time = None
            end_time = None
    elif start_time is None and end_time is None and time_range is not None:
        time_range = int(time_range)
    

    if start_time is not None and end_time is not None:
        range_filter = (start_time, end_time)
    else:
        range_filter = (timezone.now() - datetime.timedelta(minutes=time_range), timezone.now())
    available_sensor_ids = sorted(list(set(SensorData.objects.filter(sensor_timestamp__range=range_filter).values_list('sensor_id', flat=True))))
    sensor_ids = request.GET.getlist('sensors', [])
    if sensor_ids == []:
        sensor_ids = available_sensor_ids
    sensor_ids = [s for s in sensor_ids if s in available_sensor_ids]  # Make sure we only include valid sensor IDs

    return {
        'available_sensor_ids': available_sensor_ids,
        'sensor_ids': sensor_ids,
        'start_time': start_time,
        'end_time': end_time,
        'time_range': time_range,
        'real_time': real_time,
        'time_range_options': time_range_options,
        'time_range_mode': start_time is None and end_time is None,
        'real_time_mode': real_time and (start_time is None and end_time is None),
    }


def sensor_data_view(request, sensor_id):
    charts = [
        {
            'title': 'SPL',
            'data': [
                {'label': 'Leq', 'data_path': 'leq', 'color': 'blue'},
                {'label': 'LAeq', 'data_path': 'LAeq', 'color': 'red'}
            ],
            'y_min': 40,
            'y_max': 90,
            'y_unit': 'dB'
        },
        {
            'title': 'Perceptual Attributes',
            'data': [
                {'label': 'Pleasantness', 'data_path': 'pleasantness_intg', 'color': 'blue'},
                {'label': 'Pleasantness inst', 'data_path': 'pleasantness_inst', 'color': 'darkBlue', 'dash': True},
                {'label': 'Eventfulness', 'data_path': 'eventfulness_intg', 'color': 'green'},
                {'label': 'Eventfulness inst', 'data_path': 'eventfulness_inst', 'color': 'darkGreen', 'dash': True}
            ],
            'y_min': -0.5,
            'y_max': 0.5,
            'y_unit': ''
        },
        {
            'title': 'Detected Sources',
            'data': [
                {'label': 'Birds', 'data_path': 'sources.birds', 'color': 'red'},
                {'label': 'Construction', 'data_path': 'sources.construction', 'color': 'orange'},
                {'label': 'Dogs', 'data_path': 'sources.dogs', 'color': 'purple'},
                {'label': 'Human', 'data_path': 'sources.human', 'color': 'brown'},
                {'label': 'Music', 'data_path': 'sources.music', 'color': 'pink'},
                {'label': 'Nature', 'data_path': 'sources.nature', 'color': 'gray'},
                {'label': 'Siren', 'data_path': 'sources.siren', 'color': 'black'},
                {'label': 'Vehicles', 'data_path': 'sources.vehicles', 'color': 'cyan'},
            ],
            'y_min': 0.0,
            'y_max': 1.0,
            'y_unit': ''
        }
    ]
    tvars = _process_sensor_data_form(request)
    tvars.update({
        'sensor_ids': [sensor_id],
        'single_sensor': True,
        'api_endpoint_url': os.getenv('API_BASE_URL') + f'/sensor-data/',
        'charts': charts
    })
    return render(request, 'sensors/sensor_data.html', tvars)


def multiple_sensor_data_view(request):
    charts = [
        {
            'title': 'SPL - Leq',
            'data': [
                {'label': 'Leq', 'data_path': 'leq', 'color': 'blue'}
            ],
            'y_min': 40,
            'y_max': 90,
            'y_unit': 'dB'
        },
        {
            'title': 'SPL - LAeq',
            'data': [
                {'label': 'LAeq', 'data_path': 'LAeq', 'color': 'red'}
            ],
            'y_min': 40,
            'y_max': 90,
            'y_unit': 'dB'
        },
        {
            'title': 'Perceptual Attributes - Pleasantness',
            'data': [
                {'label': 'Pleasantness', 'data_path': 'pleasantness_intg', 'color': 'blue'},
                {'label': 'Pleasantness inst', 'data_path': 'pleasantness_inst', 'color': 'darkBlue', 'dash': True},
            ],
            'y_min': -0.5,
            'y_max': 0.5,
            'y_unit': ''
        },
        {
            'title': 'Perceptual Attributes - Eventfulness',
            'data': [
                {'label': 'Eventfulness', 'data_path': 'eventfulness_intg', 'color': 'green'},
                {'label': 'Eventfulness inst', 'data_path': 'eventfulness_inst', 'color': 'darkGreen', 'dash': True}
            ],
            'y_min': -0.5,
            'y_max': 0.5,
            'y_unit': ''
        }
    ]
    sources_data = [
        {'label': 'Birds', 'data_path': 'sources.birds', 'color': 'red'},
        {'label': 'Construction', 'data_path': 'sources.construction', 'color': 'orange'},
        {'label': 'Dogs', 'data_path': 'sources.dogs', 'color': 'purple'},
        {'label': 'Human', 'data_path': 'sources.human', 'color': 'brown'},
        {'label': 'Music', 'data_path': 'sources.music', 'color': 'pink'},
        {'label': 'Nature', 'data_path': 'sources.nature', 'color': 'gray'},
        {'label': 'Siren', 'data_path': 'sources.siren', 'color': 'black'},
        {'label': 'Vehicles', 'data_path': 'sources.vehicles', 'color': 'cyan'},
    ]
    for source in sources_data:
        charts.append({
            'title': f'Detected Sources - {source["label"]}',
            'data': [source],
            'y_min': 0.0,
            'y_max': 1.0,
            'y_unit': ''
        })


    tvars = _process_sensor_data_form(request)
    tvars.update({
        'single_sensor': False,
        'api_endpoint_url': os.getenv('API_BASE_URL') + f'/sensor-data/',
        'charts': charts
    })
    return render(request, 'sensors/sensor_data.html', tvars)

def frontpage(request):
    return render(request, 'sensors/frontpage.html', {
        'num_data_points': SensorData.objects.count(),
        'num_sensors': SensorData.objects.values_list('sensor_id', flat=True).distinct().count()
    })