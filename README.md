# IOT_devices_backend
BACKEND for iot devices

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
