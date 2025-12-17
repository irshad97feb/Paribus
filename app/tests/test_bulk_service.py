import pytest
from unittest.mock import patch, AsyncMock
from app.services.bulk_service import process_bulk_hospitals


@pytest.mark.asyncio
async def test_bulk_service_success():
    rows = [{"name": "A", "address": "B", "phone": "123"}]

    # Mock create_hospital & activate_batch
    with patch("app.services.bulk_service.create_hospital") as mock_create, \
         patch("app.services.bulk_service.activate_batch") as mock_activate:

        mock_create.return_value = AsyncMock(id=111)
        mock_activate.return_value = True

        result = await process_bulk_hospitals(rows)

        assert result.processed_hospitals == 1
        assert result.failed_hospitals == 0
        assert result.batch_activated is True
        assert result.hospitals[0].hospital_id == 111


@pytest.mark.asyncio
async def test_bulk_service_partial_failure():
    rows = [
        {"name": "A", "address": "B", "phone": "1"},
        {"name": "X", "address": "Y", "phone": "2"}
    ]

    with patch("app.services.bulk_service.create_hospital") as mock_create, \
         patch("app.services.bulk_service.activate_batch") as mock_activate:

        # First succeeds, second fails
        mock_create.side_effect = [AsyncMock(id=10), None]
        mock_activate.return_value = True

        result = await process_bulk_hospitals(rows)

        assert result.processed_hospitals == 1
        assert result.failed_hospitals == 1
        assert result.hospitals[1].status == "failed"
