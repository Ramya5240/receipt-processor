from fastapi import FastAPI
from controller import receipt_controller  # We’ll create this next

# Initialize FastAPI app
app = FastAPI()

# Include the router from the controller
app.include_router(receipt_controller.router)
