FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ARG http_proxy
ARG https_proxy
ARG no_proxy
ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy
ENV no_proxy=$no_proxy

COPY gui_api/requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY gui_api/app/ /app
COPY api_models/ /app/api_models