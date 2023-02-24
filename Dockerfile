# Global Dockerfile Arguments (in our CI can be overriden in ./.build-args)
ARG BUILDER_IMG=registry.kyso.io/docker/python
ARG BUILDER_TAG=3.9.16-alpine3.16

FROM ${BUILDER_IMG}:${BUILDER_TAG}

WORKDIR /app

COPY . .

RUN apk add --no-cache libressl-dev musl-dev libffi-dev gcc build-base
# RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
# RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev 

RUN pip install cython
RUN pip install -r requirements.txt

USER root

WORKDIR /app/src

CMD ["python", "subscriber.py"]
