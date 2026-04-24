FROM python:3.9-slim

WORKDIR /app

COPY serving/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY serving/ .
COPY training/ /app/training/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
