# Receipt Processing API

This project implements a FastAPI web service that processes receipts, calculates points based on various rules, and allows users to retrieve points for a given receipt ID.

## API Endpoints

### Process Receipts
- **Path**: `/receipts/process`
- **Method**: `POST`
- **Description**: This endpoint takes in a JSON receipt and returns an ID for the receipt. The ID is used to retrieve points for the receipt.

**Request Body**
```json
{
  "retailer": "string",
  "purchaseDate": "YYYY-MM-DD",
  "purchaseTime": "HH:MM",
  "items": [
    {
      "shortDescription": "string",
      "price": "string"
    }
  ],
  "total": "string"
}
```

### Example Response

```json
{
"id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

## Get Points

- **Path**: `/receipts/{id}/points`
- **Method**: `GET`
- **Description**: This endpoint retrieves the points for a receipt using the ID generated in the `/receipts/process` endpoint.
### Example Response
```json

{
"points": 32
}
```
## Points Calculation Rules
The following rules are used to calculate points for each receipt:

- **Retailer Points**: One point for each alphanumeric character in the retailer name.
- **Round Dollar Amount**: 50 points if the total is a round dollar amount (i.e., no cents).
- **Multiple of 0.25**: 25 points if the total is a multiple of 0.25.
- **Item Pair Points**: 5 points for every two items on the receipt.
- **Item Description Points**: If the length of the item description is a multiple of 3, multiply the price by 0.2, round up to the nearest integer, and add that number of points.
- **Odd Day**: 6 points if the day of the purchase date is odd.
- **Purchase Time**: 10 points if the time of purchase is between 2:00 PM and 4:00 PM.
## Setup Instructions
### Prerequisites

- **Python**: 3.8 or higher
- **FastAPI**: For building the API
- **pytest**: For testing
- **unittest.mock**: For mocking external functions and database (if needed)
- **Docker**: For containerizing the application (optional)
## Install Dependencies

You can install the necessary dependencies using pip:

```bash

pip install fastapi uvicorn pytest
```
## Run the Application

To run the FastAPI application, use the following command:

```bash

uvicorn app:app --reload
````
This will start the API on http://127.0.0.1:8000.

## Running Tests

To run the tests, including the mock tests, use the pytest tool. In your terminal, run:

```bash

pytest
```
This will run all test cases defined in `test_main.py.`

## Docker Setup (Optional)
To run the application inside Docker, follow these steps:

### Dockerfile

```dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
### requirements.txt
````
fastapi
uvicorn
pytest
````
### Build and Run Docker Container

- Build the Docker image:

```bash

docker build -t receipt-api .
```
- Run the Docker container:

```bash
docker run -d -p 8000:8000 receipt-api
```
Your API will be available at http://localhost:8000 inside the Docker container.

## Testing
The test cases are defined in `test_main.py` and use the pytest framework. To run the tests:

### Run Tests:

```bash
pytest
```
This will test the functionality of both the process_receipt and get_points endpoints.

### Test Coverage
- **Mocking**: The tests mock the calculate_points function and the receipts_db to avoid modifying real data and ensure isolated testing.
- **Assertions**: Each test checks the correctness of the API responses and validates that the correct points are awarded according to the specified rules.
### Example Test Cases
- **Valid Receipt Submission**: This test checks if the receipt is processed correctly and an ID is returned.
- **Points Calculation with Mock**: This test verifies that the points calculation works correctly and that mocked points are returned.
- **Receipt ID Lookup**: Tests the GET /receipts/{id}/points endpoint to ensure that the correct number of points is returned for a given receipt ID.
- **Invalid Receipt Lookup**: Verifies that the correct error is returned when a non-existent receipt ID is queried.
## Example Usage
Submit a Receipt

```bash

curl -X 'POST' \
'http://127.0.0.1:8000/receipts/process' \
-H 'Content-Type: application/json' \
-d '{
"retailer": "Target",
"purchaseDate": "2022-01-01",
"purchaseTime": "13:01",
"items": [
{"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
{"shortDescription": "Emil's Cheese Pizza", "price": "12.25"}
],
"total": "35.35"
}'
```
### Response:
```json

{
"id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```
### Retrieve Points

```bash
curl -X 'GET' \
'http://127.0.0.1:8000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points'
```
### Response:
```json

{
"points": 28
}
```

---

## 🚀 **ENDPOINT TESTING USING POSTMAN**

### Step 1: Set up the `POST /receipts/process` Request

1. Open Postman.
2. Create a new `POST` request.
3. Enter the URL: `http://127.0.0.1:8000/receipts/process`.
4. Go to the **Body** tab, select **raw** and set it to **JSON**.
5. Add the following JSON data to the Body to represent a sample receipt:

    ```json
    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
      ],
      "total": "35.35"
    }
    ```

6. Click **Send**.
7. You should receive a response containing a unique receipt ID. Example:

    ```json
    {
      "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
    }
    ```

### Step 2: Set up the `GET /receipts/{id}/points` Request

1. Create a new `GET` request in Postman.
2. Replace `{id}` in the URL with the receipt ID you received from the `POST /receipts/process` response.
    - Example URL: `http://127.0.0.1:8000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points`
3. Click **Send**.
4. You should receive a response containing the calculated points. Example:

    ```json
    {
      "points": 28
    }
    ```

---

### Example Postman Collection

To simplify testing, create a Postman collection with the following endpoints:

1. **Process Receipt (POST)** - for submitting a receipt.
2. **Get Points (GET)** - for retrieving points using the receipt ID.

#### Importing a Postman Collection

1. Open Postman and click **Import**.
2. Choose to **import a file** if you have exported your collection as a `.json` file.
3. Alternatively, create a new collection manually by adding the two endpoints.

---

