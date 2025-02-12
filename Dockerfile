FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir \
    'route0x[route]==0.1.1' \
    scikit-learn \
    gliner \
    gunicorn \
    uvicorn \
    fastapi

COPY assets /assets
COPY src/nlu /nlu

WORKDIR /nlu

EXPOSE 8000

# Define the command to run the app using Gunicorn with Uvicorn Workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
