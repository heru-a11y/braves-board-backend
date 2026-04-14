from pydantic import BaseModel
from typing import List
from app.schemas.column import ColumnResponse

class ColumnSingleResponse(BaseModel):
    message: str
    data: ColumnResponse

class ColumnListResponse(BaseModel):
    message: str
    data: List[ColumnResponse]