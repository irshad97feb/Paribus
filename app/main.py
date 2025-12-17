from fastapi import FastAPI
from app.routes.bulk_router import router
import httpx
from app.schemas import Hospital
from app.config import (
    GET_HOSPITALS,
    DELETE_HOSPITALS,
)

app = FastAPI(title="Hospital Bulk Processing System")

app.include_router(router)

@app.get("/hospitals")
async def get_hospitals() -> Hospital:
    async with httpx.AsyncClient() as client:
        response = await client.get(GET_HOSPITALS)
        response.raise_for_status()  # raises error if bad response
        return response.json()

@app.delete("/hospitals/batch/{batch_id}/")
async def delete_all_hospitals_batch(batch_id: str):
    # DELETE_HOSPITALS = f"DELETE_HOSPITALS/{batch_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{DELETE_HOSPITALS}/{batch_id}")
        response.raise_for_status()  # raises error if bad response
        return response.json()
