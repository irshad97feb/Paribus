import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
import io


client = TestClient(app)


def create_csv(content: str):
    return io.BytesIO(content.encode())


@pytest.mark.asyncio
def test_bulk_endpoint_success():
    csv_content = "name,address,phone\nA,B,123\nC,D,456"

    with patch("app.services.bulk_service.create_hospital") as mock_create, \
         patch("app.services.bulk_service.activate_batch") as mock_activate:

        mock_create.side_effect = [AsyncMock(id=1), AsyncMock(id=2)]
        mock_activate.return_value = True

        response = client.post(
            "/hospitals/bulk",
            files={"file": ("test.csv", create_csv(csv_content), "text/csv")}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total_hospitals"] == 2
        assert data["processed_hospitals"] == 2
        assert data["failed_hospitals"] == 0


@pytest.mark.asyncio
def test_bulk_endpoint_csv_missing_field():
    csv_content = "name,address,phone\nA,,123"

    response = client.post(
        "/hospitals/bulk",
        files={"file": ("test.csv", create_csv(csv_content), "text/csv")}
    )

    assert response.status_code == 400
