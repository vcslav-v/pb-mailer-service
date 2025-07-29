FROM python:3.13-alpine

RUN apt-get update && apt-get install -y git

ENV CONTAINER_HOME=/usr/src/app/pb-mailer-service

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt