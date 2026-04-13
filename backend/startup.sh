#!/bin/bash
# Startup command to correctly run a FastAPI app on Azure App Service
# Azure needs a WSGI server like Gunicorn, but FastAPI is an ASGI app,
# so we run Gunicorn with the Uvicorn worker class.
gunicorn --bind=0.0.0.0 --timeout 600 -k uvicorn.workers.UvicornWorker app:app
