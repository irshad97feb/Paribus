import uuid
import time
from typing import List
from app.schemas import HospitalProcessResult, BulkResponse, HospitalCreate
from app.services.hospital_api_client import create_hospital, activate_batch
import asyncio


async def process_bulk_hospitals(rows) -> BulkResponse:
    batch_id = str(uuid.uuid4())
    results: List[HospitalProcessResult] = []

    start_time = time.time()

    processed = 0
    failed = 0
    tasks = []
    row_map = {}  # track row numbers

    # Prepare async tasks
    for i, row in enumerate(rows, start=1):
        name = row.get("name")
        address = row.get("address")
        phone = row.get("phone")

        row_map[i] = name  # store mapping for later

        tasks.append(
            asyncio.create_task(create_hospital(
                HospitalCreate(
                    name=name,
                    address=address,
                    phone=phone,
                    creation_batch_id=batch_id)))
        )

    # Run all requests concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    processed = 0
    failed = 0

    for idx, response in enumerate(responses, start=1):
        name = row_map[idx]

        if isinstance(response, Exception) or response is None:
            failed += 1
            results.append(HospitalProcessResult(
                row=idx,
                hospital_id=None,
                name=name,
                status="failed"
            ))
        else:
            processed += 1
            results.append(HospitalProcessResult(
                row=idx,
                hospital_id=response.id,
                name=name,
                status="created"
            ))


    activated = await activate_batch(batch_id)

    processing_time = round(time.time() - start_time, 2)

    return BulkResponse(
        batch_id=batch_id,
        total_hospitals=len(rows),
        processed_hospitals=processed,
        failed_hospitals=failed,
        batch_activated=activated,
        processing_time_seconds=processing_time,
        hospitals=results
    )
