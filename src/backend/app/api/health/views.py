from fastapi import APIRouter
from pydantic import BaseModel
from app.api.standard_response import StandardResponse, success_response

router = APIRouter(tags=["Health Check"])

class HealthData(BaseModel):
    status: str
    message: str

@router.get("/healthz", response_model=StandardResponse[HealthData])
async def health_check():
    """
    Endpoint untuk mengecek status kesehatan aplikasi.
    Digunakan oleh Docker healthcheck atau Load Balancer.
    """
    return success_response(HealthData(
        status="ok",
        message="System is fully operational"
    ))