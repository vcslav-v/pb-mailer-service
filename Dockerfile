FROM python:3.13-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    build-base

ENV CONTAINER_HOME=/usr/src/app/pb-mailer-service

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt