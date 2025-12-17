from fastapi import UploadFile, HTTPException

async def parse_csv(file: UploadFile):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type, only CSV allowed")

    # Decode and remove BOM if present
    text = (await file.read()).decode("utf-8-sig").strip()

    lines = text.split("\n")
    print("lines",lines)
    if len(lines) < 2:
        raise HTTPException(status_code=400, detail="CSV must contain at least one data row")
    if len(lines)  > 20:
        raise HTTPException(status_code=400, detail="CSV cannot contain more than 20 hospitals")

    # Header validation
    headers = [h.strip() for h in lines[0].split(",")]
    required_headers = {"name", "address", "phone"}

    if not required_headers.issubset(set(headers)):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain headers: {', '.join(required_headers)}"
        )

    rows = []
    header_len = len(headers)

    row_count = 0

    for line in lines[1:]:
        if row_count >= 20:
            break  # enforce max 20 rows

        line = line.strip()
        if not line:
            continue  # skip empty lines

        values = [v.strip() for v in line.split(",")]

        # pad or trim to match header length
        if len(values) < header_len:
            values += [""] * (header_len - len(values))
        elif len(values) > header_len:
            values = values[:header_len]

        # required values check
        if not values[0] or not values[1]:  # name, address required
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields in CSV row {row_count + 1}"
            )

        rows.append(dict(zip(headers, values)))
        row_count += 1

    return rows