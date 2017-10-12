FROM python:3.6.3-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

RUN pip install \
    psutil \
    pyyaml

COPY probe.py /app

ENTRYPOINT ["python", "probe.py"]
