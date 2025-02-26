# src/main.py
import uvicorn
from fastapi import FastAPI
from src.api.endpoints import setup_api  # Import the setup function

# Create the FastAPI app instance
app = FastAPI()

# Attach the API endpoints
setup_api(app)

if __name__ == "__main__":
    # Run the app using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)