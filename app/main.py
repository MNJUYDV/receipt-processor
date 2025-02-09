from fastapi import FastAPI
from app.api.endpoints import receipts

app = FastAPI(title="Receipt Processor")

app.include_router(receipts.router, prefix="/receipts", tags=["receipts"])

@app.get("/")
async def root():
    return {"message": "Receipt Processor API"}