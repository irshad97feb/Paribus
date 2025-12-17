import pytest
from fastapi import UploadFile
from app.utils import parse_csv
from fastapi import HTTPException
import io
# import asyncio


def create_file(content: str, name="test.csv"):
    return UploadFile(filename=name, file=io.BytesIO(content.encode()))


@pytest.mark.asyncio
async def test_valid_csv():
    file = create_file("name,address,phone\nA,B,123\nC,D,456")
    rows = await parse_csv(file)
    assert len(rows) == 2
    assert rows[0]["name"] == "A"
    assert rows[1]["address"] == "D"


@pytest.mark.asyncio
async def test_invalid_extension():
    file = create_file("name,address,phone\nA,B,1", name="data.txt")
    with pytest.raises(HTTPException):
        await parse_csv(file)


@pytest.mark.asyncio
async def test_missing_headers():
    file = create_file("name,address\nA,B")
    with pytest.raises(HTTPException):
        await parse_csv(file)


@pytest.mark.asyncio
async def test_empty_rows_skipped():
    file = create_file("name,address,phone\nA,B,1\n\nC,D,2")
    rows = await parse_csv(file)
    assert len(rows) == 2


@pytest.mark.asyncio
async def test_max_20_rows():
    lines = ["name,address,phone"]
    for i in range(25):
        lines.append(f"A{i},B{i},12345")

    file = create_file("\n".join(lines))
    with pytest.raises(HTTPException):
        await parse_csv(file)
