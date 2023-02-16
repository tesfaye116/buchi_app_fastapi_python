#write dockerfile for fast api and mongo db

FROM python:3.10.6 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]

# Path: docker-compose.yml






