FROM python:3.11-alpine

RUN apk update && apk add --no-cache build-base

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements/base.txt

