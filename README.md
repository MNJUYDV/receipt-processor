# Receipt Processor

## Running with Docker

### Prerequisites
- Docker
- Docker Compose

### Building and Running

1. Build and start the container:
```bash
docker-compose up --build
```

2. Access the API:
- Main API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Running Tests in Docker

1. Build and run tests:
```bash
docker-compose run web pytest
```

2. Run specific test file:
```bash
docker-compose run web pytest tests/test_receipt_api.py -v
```

### Development with Docker

1. The application code is mounted as a volume, so changes will be reflected immediately with the --reload flag enabled.

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the containers:
```bash
docker-compose down
```

## Manual Setup (without Docker)

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Run tests:
```bash
pytest
```

## API Documentation

### Endpoints

1. Process Receipt
- POST `/receipts/process`
- Accepts a receipt JSON and returns an ID

2. Get Points
- GET `/receipts/{id}/points`
- Returns the points awarded for the receipt