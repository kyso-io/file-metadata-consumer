FROM registry.kyso.io/docker/kyso-file-metadata-postprocess-builder/main:latest

WORKDIR /app

RUN mkdir data

COPY . .

USER root

WORKDIR /app/src

ENV PYTHONUNBUFFERED=1

CMD ["python", "subscriber.py"]
