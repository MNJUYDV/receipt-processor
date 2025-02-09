# Receipt Processor

A FastAPI application that processes receipts and calculates reward points based on various rules.

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

### Endpoints

1. Process Receipt
   - POST `/receipts/process`
   - Accepts a receipt JSON and returns an ID

2. Get Points
   - GET `/receipts/{id}/points`
   - Returns the points awarded for the receipt

## Running Tests

Execute tests using pytest:
```bash
pytest
```

## Project Structure

```
receipt_processor/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configuration
│   ├── models/         # Pydantic models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
└── tests/              # Test files
```