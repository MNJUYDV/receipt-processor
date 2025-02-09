from pydantic import BaseModel, Field
from typing import List
from datetime import date, time

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: str

class ReceiptResponse(BaseModel):
    id: str

class PointsResponse(BaseModel):
    points: int