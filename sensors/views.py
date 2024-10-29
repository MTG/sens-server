from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import SensorData
from .serializers import SensorDataSerializer
from django.utils.dateparse import parse_datetime
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
    sensor_data = SensorData.objects.filter(Q(timestamp__gte=start_datetime) & Q(timestamp__lte=end_datetime))

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
        timestamp__gte=start_datetime,
        timestamp__lte=end_datetime
    )

    # Serialize and return the filtered data
    serializer = SensorDataSerializer(sensor_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_sensor_ids(request):
    # Retrieve distinct sensor IDs from the SensorData model
    sensor_ids = SensorData.objects.values_list('sensor_id', flat=True).distinct()

    # Return the list of sensor IDs
    return Response(list(sensor_ids), status=status.HTTP_200_OK)


def sensor_data_view(request, sensor_id):
    # Get query parameters for date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse the start and end dates if provided
    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    # Build the filter query
    filter_query = Q(sensor_id=sensor_id)
    
    if start_date:
        filter_query &= Q(timestamp__gte=start_date)
    if end_date:
        filter_query &= Q(timestamp__lte=end_date)

    # Retrieve the filtered sensor data
    sensor_data = SensorData.objects.filter(filter_query).order_by('timestamp')

    # Render the data using a template
    return render(request, 'sensors/sensor_data.html', {
        'sensor_data': sensor_data,
        'sensor_id': sensor_id,
        'start_date': start_date,
        'end_date': end_date
    })


def frontpage(request):
    return render(request, 'sensors/frontpage.html', {
        'num_data_points': SensorData.objects.count(),
        'num_sensors': SensorData.objects.values_list('sensor_id', flat=True).distinct().count()
    })