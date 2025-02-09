from fastapi import APIRouter, HTTPException
from app.models.receipt import Receipt, ReceiptResponse, PointsResponse
from app.services.receipt_service import receipt_service

router = APIRouter()

@router.post("/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    receipt_id = receipt_service.process_receipt(receipt)
    return ReceiptResponse(id=receipt_id)

@router.get("/{id}/points", response_model=PointsResponse)
async def get_points(id: str):
    points = receipt_service.get_points(id)
    if points is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return PointsResponse(points=points)