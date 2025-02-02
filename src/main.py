"""
Main module to initialize and run the FastAPI application.

This module sets up the FastAPI application, includes API routes from the 'api' module,
and runs the Uvicorn server when executed as the main module.
"""

import uvicorn
from fastapi import FastAPI
from .api import app as api_app  # Import the API instance from the api module

# Create the main FastAPI application instance
app = FastAPI()

# Include the endpoints defined in the API module
app.include_router(api_app.router)

if __name__ == "__main__":
    # Run the Uvicorn server to host the FastAPI application
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
