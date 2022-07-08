FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG pip_install_options

ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy
ENV no_proxy=$no_proxy

COPY db_api/requirements.txt .
RUN pip install -r requirements.txt ${pip_install_options}

COPY db_api/app/ /app
COPY api_models/ /app/api_models