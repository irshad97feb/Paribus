from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class Hospital(BaseModel):
    id: int
    name: str
    address: str
    phone: Optional[str]
    creation_batch_id: Optional[str]
    active: bool
    created_at: datetime


class HospitalCreate(BaseModel):
    name: str
    address: str
    phone: Optional[str]
    creation_batch_id: Optional[str]


class HospitalUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]


class ValidationError(BaseModel):
    loc: List[Any]
    msg: str
    type: str


class HospitalProcessResult(BaseModel):
    row: int
    hospital_id: Optional[int]
    name: str
    status: str


class BulkResponse(BaseModel):
    batch_id: str
    total_hospitals: int
    processed_hospitals: int
    failed_hospitals: int
    processing_time_seconds: float
    batch_activated: bool
    hospitals: List[HospitalProcessResult]