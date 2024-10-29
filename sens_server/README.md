# SENS server


To post data:

```
curl -X POST http://127.0.0.1:8000/api/sensor-data/ \
-H "Content-Type: application/json" \
-d '{"sensor_id": "sensor_123", "location": "Building A", "data": {"pleasantness": 0.62, "eventfulness": 0.8, "sources":{"dog":0.7}}}'
```

To retrieve data from a sensor:

```
curl http://127.0.0.1:8000/api/sensor-data/sensor_123/
```