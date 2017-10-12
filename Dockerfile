FROM python:3.6.3-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk add --no-cache --virtual build_dependencies \
      gcc \
      musl-dev \
      linux-headers \
 && pip install --no-cache-dir \
      psutil \
      pyyaml \
 && apk del build_dependencies

COPY probe.py /app

ENTRYPOINT ["python", "probe.py"]
