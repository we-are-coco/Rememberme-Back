# Use an official Python base image as a parent image
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN apt update
RUN apt install -y pkg-config ffmpeg default-libmysqlclient-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]