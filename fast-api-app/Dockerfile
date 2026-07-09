FROM python:3.13-slim

WORKDIR fast-api-app

COPY fast-api-app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY fast-api-app/ .
COPY .env ../

# Run tests to ensure the environment is ready
# RUN pytest tests/backend_health_test.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
