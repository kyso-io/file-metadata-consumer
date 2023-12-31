FROM python:3.9.16-alpine3.16

WORKDIR /app

COPY . .

RUN apk add --no-cache libressl-dev musl-dev libffi-dev gcc build-base
# RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
# RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev 

RUN pip install cython
RUN pip install -r requirements.txt

WORKDIR /app

RUN mkdir data

COPY . .

USER root

WORKDIR /app/src

ENV PYTHONUNBUFFERED=1

CMD ["python", "subscriber.py"]
