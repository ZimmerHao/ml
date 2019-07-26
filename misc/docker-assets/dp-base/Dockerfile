FROM python:3.7.3-alpine
ARG MODE
RUN apk update && \
    apk add --no-cache --virtual .build-deps libffi-dev openssl-dev libxslt-dev libxml2-dev libc-dev zlib-dev postgresql-dev gcc python3-dev musl-dev libxml2 libc-dev  && \
    apk add libpq && \
    apk add libxslt-dev && \
    pip install cython
RUN mkdir /requirements
ADD requirements/common.txt /requirements
RUN pip install -r /requirements/common.txt --no-cache-dir && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*
