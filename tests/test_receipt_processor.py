from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app instance

# Create the TestClient for making requests to the FastAPI app
client = TestClient(app)

def test_root():
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Receipt processor is up and running!"}

def test_process_receipt():
    # Sample receipt data to post
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ],
        "total": "35.35"
    }

    # Send a POST request to the /receipts/process endpoint
    response = client.post("/receipts/process", json=receipt_data)

    # Assert that the response contains the ID and is a valid 200 status code
    assert response.status_code == 200
    assert "id" in response.json()

    # Now that we have the receipt ID, let's test the get points endpoint
    receipt_id = response.json()["id"]
    points_response = client.get(f"/receipts/{receipt_id}/points")

    # Assert that we get the expected points (28 points from the earlier calculation)
    assert points_response.status_code == 200
    assert points_response.json() == {"points": 28}

def test_invalid_receipt():
    # Test sending a malformed receipt (missing required fields)
    invalid_receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01"
        # Missing 'purchaseTime' and 'items'
    }
    response = client.post("/receipts/process", json=invalid_receipt)
    
    # Check if the response code is 422 for unprocessable entity
    assert response.status_code == 422

