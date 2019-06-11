FROM python:3.7.3-alpine
ARG MODE
RUN apk update && \
    apk add --no-cache --virtual .build-deps libffi-dev openssl-dev libxslt-dev libxml2-dev libc-dev zlib-dev postgresql-dev gcc python3-dev musl-dev  && \
    apk add libpq && \
    pip install cython
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/$MODE.txt --no-cache-dir && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*
