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


## API

### Post sensor data

You can post data making a POST request like this:

    curl -X POST http://127.0.0.1:8000/sens/api/sensor-data/ -H "Content-Type: application/json" -d '{"uuid": "18963ff9-77a2-4f75-b427-0d92bca78da5", "sensor_id": "sensor_124", "location": "Building A", "data": {"pleasantness": 0.62, "eventfulness": 0.8, "sources":{"dog":0.7}}}'

The contents of the `sensor_id`, `location` are strings. `data` field can contain arbitrary JSON formatted data.


### List sensor IDs

    curl "http://localhost:8000/sens/api/sensor-data/sensor-ids/"


### Get data points for sensor

You can retrieve the data points posted by a specific sensor using its ID.

    curl "http://localhost:8000/sens/api/sensor-data/<SENSOR_ID>/


You can also filter the data points by time range.

    curl "http://localhost:8000/sens/api/sensor-data/<SENSOR_ID>/time-range/?start_date=2023-10-01T00:00:00Z&end_date=2025-10-10T23:59:59Z"


### Get data points for all sensors

You cna retrieve data points posted by all connected servers during a specific time range.

    curl "http://localhost:8000/sens/api/sensor-data/time-range/?start_date=2023-10-01T00:00:00Z&end_date=2025-10-10T23:59:59Z"