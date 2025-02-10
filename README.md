# Receipt Processor

A FastAPI service that processes receipts and calculates points based on specific rules. The service allows you to submit receipts and retrieve their point values.

## Setup and Run

### Using Docker
```bash
# Build and run
docker-compose up --build

# Stop
docker-compose down
```

### Without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Run tests
pytest
```

## API Endpoints

### 1. Process Receipt
POST `/receipts/process`

Request body example:
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    }
  ],
  "total": "6.49"
}
```

Response:
```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### 2. Get Points
GET `/receipts/{id}/points`

Response:
```json
{
  "points": 32
}
```

Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc