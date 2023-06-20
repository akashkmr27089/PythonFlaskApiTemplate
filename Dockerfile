FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
