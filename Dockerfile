FROM python:3.6.3-alpine

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile* /app/
COPY probe.py /app/

RUN apk add --no-cache --virtual build_dependencies \
      gcc \
      musl-dev \
      linux-headers \
 && pip install --quiet --no-cache-dir pipenv \
 && pipenv install --ignore-pipfile --system \
 && apk del build_dependencies

ENTRYPOINT ["python", "/app/probe.py"]
