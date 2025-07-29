FROM python:3.13-alpine

RUN mkdir -p /usr/src/app/pb-mailer-service

ENV CONTAINER_HOME=/usr/src/app/pb-mailer-service

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "pb-mailer-service/main.py"]