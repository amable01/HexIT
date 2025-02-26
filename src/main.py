# src/main.py
import uvicorn
from src.api.endpoints import app  # Import the app directly

if __name__ == "__main__":
    # Run the app using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)