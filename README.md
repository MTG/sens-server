# sens-server

Server-side infrastructure for SENS acoustic sensors


## Steps to setup local installation

1. Clone repository

    git clone git@github.com:MTG/sens-server.git
    cd sens-server


2. Build docker images

    docker compose build


3. Run server!

    docker compose up


4. Apply database migrations, create super user (run these in a separate terminal while `docker compose up` is running)

    docker compose run --rm web python manage.py migrate
    docker compose run --rm web python manage.py createsuperuser


5. You should now be able to access the server at `http://localhost:8000/sens/`

6. You can visit the admin site (log in with the superuser account) at `http://localhost:8000/sens/admin/`


## Steps to deploy

1. Run following deploy command:

    docker compose run --rm web fab deploy


Note this needs to done from a server that has access to `fs-labs.s.upf.edu`.


## API

### Post sensor data

You can post data making a POST request like this:

    curl -X POST http://localhost:8800/sens/api/sensor-data/ -H "Content-Type: application/json" -d '{"sensor_timestamp":"2024-08-01T14:38:36", "uuid": "18963ff9-77a2-4f75-b427-0d92bca78da5", "sensor_id": "sensor_124", "location": "Building A", "data": {"pleasantness": 0.62, "eventfulness": 0.8, "sources":{"dog":0.7}}}'

The contents of the `sensor_id`, `location` are strings. `data` field can contain arbitrary JSON formatted data.


### List sensor IDs

    curl "http://localhost:8800/sens/api/sensor-data/sensor-ids/"


### Get data points for sensor

You can retrieve the data points posted by a specific sensor using its ID.

    curl "http://localhost:8800/sens/api/sensor-data/<SENSOR_ID>/


You can also filter the data points by time range.

    curl "http://localhost:8800/sens/api/sensor-data/<SENSOR_ID>/time-range/?start_date=2023-10-01T00:00:00Z&end_date=2025-10-10T23:59:59Z"


### Get data points for all sensors

You can retrieve data points posted by all connected servers during a specific time range.

    curl "http://localhost:8800/sens/api/sensor-data/time-range/?start_date=2023-10-01T00:00:00Z&end_date=2025-10-10T23:59:59Z"


## Pythyon client

A very simple Python client is included which can be used to interact with the server. Here are usage examples using the client:

    import client
    import datetime
    
    # Method to post data to the server (sensors use this method to send data to the remote server)
    client.post_sensor_data({"pleasantness": 0.85, "eventfulness": 0.3, "sources": {"bird": 0.5, "car": 0.2}})
    
    # Methods to retrieve sensor data from the server
    client.get_sensor_ids()
    client.get_sensors_data(start_date=datetime.datetime(2023,1,1), end_date=datetime.datetime(2025,3,5,22,13))
    client.get_data_for_sensor_id(sensor_id='sensor1')
    client.get_data_for_sensor_id(sensor_id='sensor1', start_date=datetime.datetime(2023,1,1), end_date=datetime.datetime(2025,3,5,22,13))


Data points posted using the `post_sensor_data` method will include sensor ID and sensor location information which will be loaded from existing files `sensor_id.txt` and `location.txt` which should be placed at the directory from which the Python code is run from. If these files do not exist, sensor ID and location will be set to `"unknown"`. `sensor_id.txt` and `location.txt` can include an arbitrary string.