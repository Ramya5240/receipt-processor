from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator  # Use field_validator from Pydantic
from typing import List, Dict
import uuid
from datetime import datetime

app = FastAPI()
receipts_db = {}

# Pydantic model for individual items in the receipt
class Item(BaseModel):
    shortDescription: str = Field(..., pattern="^[\\w\\s\\-]+$")
    price: str = Field(..., pattern="^\\d+\\.\\d{2}$")

# Pydantic model for receipt data
class Receipt(BaseModel):
    retailer: str = Field(..., pattern="^[\\w\\s\\-&]+$")
    purchaseDate: str  # This will be validated in the validator
    purchaseTime: str  # This will be validated in the validator
    items: List[Item]
    total: str = Field(..., pattern="^\\d+\\.\\d{2}$")

    # Updated to use field_validator for date validation
    @field_validator('purchaseDate')
    def validate_purchase_date(cls, value):
        # Validate that the date is in YYYY-MM-DD format and is a valid calendar date
        try:
            datetime.strptime(value, "%Y-%m-%d")  # Ensures valid date
        except ValueError:
            raise ValueError('purchaseDate must be a valid date in YYYY-MM-DD format')
        return value

    @field_validator('purchaseTime')
    def validate_purchase_time(cls, value):
        # Validate that the time is in HH:MM format
        parts = value.split(':')
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise ValueError('purchaseTime must be in HH:MM format')
        hour, minute = map(int, parts)
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError('purchaseTime must be a valid time (HH:MM)')
        return value

# Pydantic model for response when a receipt is processed
class ReceiptResponse(BaseModel):
    id: str

# Pydantic model for response with points
class PointsResponse(BaseModel):
    points: int

# Function to calculate points based on the receipt
def calculate_points(receipt: Receipt) -> int:
    points = 0

    # Rule 1: Points based on retailer name (length of retailer name)
    points += len(receipt.retailer)

    # Rule 2: Points if the total is a round dollar amount (no cents)
    if '.' not in receipt.total:  # No cents
        points += 50

    # Rule 3: Points if the total is a multiple of 0.25
    try:
        total_amount = float(receipt.total)
        if total_amount % 0.25 == 0:
            points += 25
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid total price")

    # Rule 4: Points for every 2 items on the receipt (5 points per pair)
    points += (len(receipt.items) // 2) * 5

    # Rule 5: Item description length multiple of 3 => price * 0.2 (rounded up) for points
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            item_price = float(item.price)
            item_points = round(item_price * 0.2)
            points += item_points

    # Rule 6: Points if purchase date day is odd
    day_of_purchase = int(receipt.purchaseDate.split('-')[2])
    if day_of_purchase % 2 == 1:
        points += 6

    # Rule 7: Points if purchase time is between 2:00 PM and 4:00 PM
    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10

    return points

# POST endpoint to process receipt and store it
@app.post("/receipts/process", response_model=ReceiptResponse, status_code=200)
def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts_db[receipt_id] = points
    return {"id": receipt_id}

# GET endpoint to fetch points for a specific receipt
@app.get("/receipts/{receipt_id}/points", response_model=PointsResponse)
def get_points(receipt_id: str):
    if receipt_id not in receipts_db:
        raise HTTPException(status_code=404, detail="Receipt ID not found")
    return {"points": receipts_db[receipt_id]}
