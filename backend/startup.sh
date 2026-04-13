#!/bin/bash
# Azure App Service Startup Script for FastAPI
# Changes directory to backend (if not already there) and starts the server

# If the root of the repo is deployed, move into the backend folder
if [ -d "backend" ]; then
    cd backend
fi

# Run Gunicorn with Uvicorn workers on port 8000 (Azure will proxy this)
gunicorn --bind=0.0.0.0:8000 --timeout 600 -k uvicorn.workers.UvicornWorker app:app
