FROM qimo/python3.7:latest
ARG MODE
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements/$MODE.txt
