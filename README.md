# Paribus

Fast API Pribus project

# Paribus Project Directory Structure

    Paribus/
    │
    ├── app/                          # Main application package
    │   │
    │   ├── main.py                   # FastAPI entrypoint, loads routes, creates app instance
    │   ├── config.py                 # External API URLs + environment/global config
    │   ├── schemas.py                # Pydantic models for validations & API responses
    │   ├── utils.py                  # CSV parsing + validation functions
    │   │
    │   ├── routes/                   # All API endpoints grouped logically
    │   │   └── bulk_router.py        # /hospitals/bulk endpoint router
    │   │
    │   ├── services/                     # Business logic + external API interactions
    │   │   ├── bulk_service.py           # Bulk creation workflow using async + concurrency
    │   │   └── hospital_api_client.py    # HTTP client for external Hospital Directory API
    │   │
    │   └── __init__.py                   # Makes 'app' a Python package
    │
    ├── tests/                         # Pytest test suite
    │   ├── test_csv_parser.py         # Tests CSV parsing, header validation, max rows, edge cases
    │   ├── test_bulk_service.py       # Tests async workflow, success/failure handling, activation logic
    │   └── test_bulk_endpoint.py      # End-to-end API tests (mocking external API calls)
    │
    ├── Dockerfile               # Docker build instructions to containerize the app
    ├── requirements.txt         # Python package dependencies (FastAPI, httpx, uvicorn, pytest, etc.)
    ├── README.md                # Project documentation, run instructions, examples
    └── .gitignore

## CSV Format

    name,address,phone
    Apollo Hospital,Hyderabad,9999999999
    Continental Hospital,Bangalore,
    Care Hospital,Chennai,8887776666

## How to Run the Application

### Install dependencies

    pip install -r requirements.txt

### Start the FastAPI server

    uvicorn app.main:app --reload

Server runs at: http://localhost:8000/docs (Swagger UI)

## Running Tests

    pytest -q

## Run with Docker

### Build the Docker image

    docker build -t hospital-bulk-api .

### Run container

    docker run -p 8000:8000 hospital-bulk-api

## API Endpoint

**POST /hospitals/bulk**

Uploads a CSV and returns batch processing summary.

### Example Response

    {
      "batch_id": "uuid",
      "total_hospitals": 10,
      "processed_hospitals": 9,
      "failed_hospitals": 1,
      "processing_time_seconds": 5.9,
      "batch_activated": true,
      "hospitals": [
        { "row": 1, "hospital_id": 101, "name": "Apollo", "status": "created" },
        { "row": 2, "hospital_id": null, "name": "Continental", "status": "failed" }
      ]
    }
