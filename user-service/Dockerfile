FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /user-service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
