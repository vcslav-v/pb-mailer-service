FROM python:3.13-slim

RUN apt-get update

ENV CONTAINER_HOME=/usr/src/app/pb-mailer-service

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt