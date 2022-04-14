FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY db_api/requirements.txt .
RUN pip install -r requirements.txt

COPY db_api/app/ /app
COPY api_models/ /app/api_models