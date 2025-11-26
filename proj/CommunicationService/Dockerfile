FROM python:3.13-slim

WORKDIR /app

# Copy requirements from CommunicationService
COPY ./CommunicationService/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy Cache module (shared dependency)
COPY ./Cache ./Cache

# Copy CommunicationService application code
COPY ./CommunicationService/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
