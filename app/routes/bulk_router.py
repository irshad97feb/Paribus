from fastapi import APIRouter, UploadFile, File
from app.utils import parse_csv
from app.services.bulk_service import process_bulk_hospitals
import httpx
from app.schemas import BulkResponse

router = APIRouter()
HOSPITAL_API = "https://hospital-directory.onrender.com/hospitals/"


@router.post("/hospitals/bulk")
async def bulk_process(file: UploadFile = File(...)) -> BulkResponse:
    try:
        rows = await parse_csv(file)
        result = await process_bulk_hospitals(rows)
        return result
    except httpx.HTTPStatusError as exc:
        return {"error": f"External API failed: {exc.response.text}"}
