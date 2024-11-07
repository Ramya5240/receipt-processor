import pytest
from fastapi.testclient import TestClient
from app import app, receipts_db, calculate_points, Item, Receipt, PointsResponse, ReceiptResponse

client = TestClient(app)

# Helper function to calculate expected points based on given logic
def expected_points(receipt):
    points = 0
    points += len(receipt.retailer)
    if '.' not in receipt.total:
        points += 50
    try:
        total_amount = float(receipt.total)
        if total_amount % 0.25 == 0:
            points += 25
    except ValueError:
        raise ValueError("Invalid total price")

    points += (len(receipt.items) // 2) * 5
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            item_price = float(item.price)
            item_points = round(item_price * 0.2)
            points += item_points
    day_of_purchase = int(receipt.purchaseDate.split('-')[2])
    if day_of_purchase % 2 == 1:
        points += 6
    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10
    return points

# Test: Process receipt and get points (valid case)
def test_process_receipt_valid():
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    }

    # Send POST request to process the receipt
    post_response = client.post("/receipts/process", json=receipt_data)
    assert post_response.status_code == 200
    receipt_id = post_response.json()["id"]

    # Send GET request to retrieve the points
    get_response = client.get(f"/receipts/{receipt_id}/points")
    assert get_response.status_code == 200

    # Check if the response contains the 'points' field and verify the points
    response_data = get_response.json()
    assert "points" in response_data
    assert response_data["points"] == expected_points(Receipt(**receipt_data))

# Test: Process receipt with invalid date format
def test_process_receipt_invalid_date():
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-32",  # Invalid date
        "purchaseTime": "14:33",
        "items": [{"shortDescription": "Gatorade", "price": "2.25"}],
        "total": "9.00"
    }

    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 422  # Unprocessable Entity

# Test: Process receipt with invalid time format
def test_process_receipt_invalid_time():
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "25:00",  # Invalid time
        "items": [{"shortDescription": "Gatorade", "price": "2.25"}],
        "total": "9.00"
    }

    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 422  # Unprocessable Entity

# Test: Process receipt with invalid total price format
def test_process_receipt_invalid_total():
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [{"shortDescription": "Gatorade", "price": "2.25"}],
        "total": "9"  # Invalid total (should be a decimal with two places)
    }