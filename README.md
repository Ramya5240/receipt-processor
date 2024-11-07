# Receipt Processor

The **Receipt Processor** is a FastAPI application that processes receipts, calculates reward points based on various rules, and stores receipt data in memory. It also exposes API endpoints for processing receipts and retrieving the calculated points.

## Table of Contents

- [Installation](#installation)
- [Run the FastAPI Server](#run-the-fastapi-server)
- [Run the Tests](#run-the-tests)
- [API Endpoints](#api-endpoints)
- [Docker Deployment](#docker-deployment)

## Installation

Follow these steps to get the project up and running on your local machine.

1. **Clone the Repository**

   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/receipt-processor.git
### Install Dependencies
Make sure you have Python 3.9 or later installed. Then, install the requried Python packages:
```bash
pip install -r requirements.txt
```
## Run the FastAPI Server
Once the dependencies are installed, you can run the FastAPI server using uvicorn.
1. Run the FastAPI server
```bash
uvicorn main:app --reload
```
2. The server will start at ```` http://127.0.0.1:8000````. You can access the application and API endpoints at this address.
## Run the Tests
To ensure that everything is working correctly, you can run the tests using pytest.

1. Install testing dependencies (if not already installed):
````bash
pip install pytest
````
2. Run the tests:
````bash
pytest
````
This will execute all the tests in the project and display the results in the terminal.
## API Endpoints
1. ### Process Receipt (POST /receipts/process)
- **Description**: This endpoint receives a receipt in JSON format, calculates reward points, and returns a unique receipt ID.
- **Request Example**:
````bash
{
  "retailer": "SuperMart",
  "total": 50.00,
  "purchaseDate": "2024-11-06",
  "purchaseTime": "15:30",
  "items": [
    {
      "shortDescription": "Item 1",
      "price": 10.00
    },
    {
      "shortDescription": "Item 2",
      "price": 20.00
    }
  ]
}
````
- **Response Example**:
````json
{
  "id": "unique-receipt-id"
}
````
2. ### Get Points (GET /receipts/{id}/points)
- **Description**:This endpoint retrieves the reward points for a specific receipt using its unique ID.
- **Request Example**:
````GET /receipts/unique-receipt-id/points````
- **Response Example**:
````json
{
  "points": 28
}
````
## Docker Deployment
You can also run the application inside a Docker container.
1. #### Build the Docker Image:
````bash
docker build -t receipt-processor .
````
2. #### Run the Docker Container:
````bash
docker run -d -p 8000:8000 receipt-processor
````
3. The application will be available at `http://localhost:8000.`
### Known Issues
- Make sure that the port `8000` is not in use by any other application before starting the container.
