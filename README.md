# Paribus
Fast API Pribus project

Directory Structure:

app/
│
├── main.py                        # FastAPI entrypoint
├── config.py                      # External API URLs
├── schemas.py                     # Pydantic models
├── utils.py                       # CSV parsing + validation
│
├── routes/
│   └── bulk_router.py             # /hospitals/bulk endpoint
│
├── services/
│   ├── bulk_service.py            # Bulk processing workflow
│   └── hospital_api_client.py     # External API calls
│
└── tests/                         # pytest test suite


# CSV Format

name,address,phone
Apollo Hospital,Hyderabad,9999999999
Continental Hospital,Bangalore,
Care Hospital,Chennai,8887776666

# How to Run the Application

## Install dependencies
pip install -r requirements.txt

## Start the FastAPI server
uvicorn app.main:app --reload


Server runs at:

http://localhost:8000/docs (Swagger UI)

# Running Tests

pytest -q

# Run with Docker
## Build the Docker image
docker build -t hospital-bulk-api .

## Run container
docker run -p 8000:8000 hospital-bulk-api

# API Endpoint

POST /hospitals/bulk

Uploads a CSV and returns batch processing summary.

Example Response

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
