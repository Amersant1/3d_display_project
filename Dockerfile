FROM python:3.11-slim

ENV PYTHONBUFFERED 1

WORKDIR /

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x ./web.sh