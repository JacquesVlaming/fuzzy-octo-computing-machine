FROM python:3.11-slim

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY src/fetch_v1.0.py .

CMD ["python", "fetch_v1.0.py"]
