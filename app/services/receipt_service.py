import uuid
from typing import Dict, Optional
from app.models.receipt import Receipt
from app.utils.points_calculator import calculate_points

class ReceiptService:
    def __init__(self):
        self.receipts: Dict[str, Receipt] = {}
        self.points_cache: Dict[str, int] = {}
    
    def process_receipt(self, receipt: Receipt) -> str:
        receipt_id = str(uuid.uuid4())
        self.receipts[receipt_id] = receipt
        # Calculate points immediately and cache them
        self.points_cache[receipt_id] = calculate_points(receipt)
        return receipt_id
    
    def get_points(self, receipt_id: str) -> Optional[int]:
        if receipt_id not in self.points_cache:
            return None
        return self.points_cache[receipt_id]

# Global instance for the application
receipt_service = ReceiptService()