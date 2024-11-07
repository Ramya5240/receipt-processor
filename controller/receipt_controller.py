from fastapi import APIRouter, HTTPException
from controller.receipt_model import Receipt  # Import the Receipt model
import uuid  # To generate unique receipt IDs
from service import receipt_service  # Import the service layer for processing

# Define a new router for receipts
router = APIRouter()

# Placeholder endpoint for testing
@router.get("/")
async def root():
    return {"message": "Receipt processor is up and running!"}

# Endpoint to process the receipt and generate a unique ID
@router.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    # Generate a unique ID for the receipt
    receipt_id = str(uuid.uuid4())
    # Calculate points using the service layer
    points = receipt_service.calculate_points(receipt)
    # Store the receipt data in memory (repository layer)
    receipt_service.store_receipt(receipt_id, points)
    # Return the generated ID
    return {"id": receipt_id}

# Endpoint to retrieve points for a specific receipt by ID
@router.get("/receipts/{id}/points")
async def get_receipt_points(id: str):
    # Retrieve points from the service layer
    points = receipt_service.get_points(id)
    # Check if the receipt ID exists
    if points is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    # Return the points in JSON format
    return {"points": points}
