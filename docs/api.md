# RF Sentinel API Reference

## Authentication

Currently no authentication required. JWT auth planned for v1.0.

## Endpoints

### Health Check

```http
GET /health
```

Response:
```json
{"status": "healthy", "version": "0.1.0"}
```

### Start Scan

```http
POST /scan
Content-Type: application/json

{
  "start_frequency": 100000000.0,
  "stop_frequency": 200000000.0,
  "step": 1000000.0,
  "dwell_time": 0.1,
  "sample_rate": 10000000.0
}
```

### Get Capture

```http
GET /capture/{id}
```

### List Captures

```http
GET /capture?limit=100&offset=0
```

### Export Capture

```http
POST /export/pdf
Content-Type: application/json

{"capture_id": 1}
```

### WebSocket Stream

Planned for real-time spectrum streaming.

## Error Codes

- 400: Bad request
- 404: Not found
- 500: Internal error