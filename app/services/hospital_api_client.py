import httpx
from app.config import (
    CREATE_HOSPITAL_URL,
    ACTIVATE_BATCH_URL,
)
from app.schemas import HospitalCreate, Hospital
        
client = httpx.AsyncClient(
    timeout=15,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
)

async def create_hospital(data: HospitalCreate):
    try:
        response = await client.post(
            CREATE_HOSPITAL_URL,
            json=data.model_dump()
        )
        if response.status_code != 200:
            return None

        return Hospital(**response.json())
    except:
        return None

async def activate_batch(batch_id):
    try:
        response = await client.patch(
            f"{ACTIVATE_BATCH_URL}/{batch_id}/activate"
        )
        return response.status_code == 200
    except Exception:
        return False