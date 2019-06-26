FROM wangxisea/dp:base
ARG MODE

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/$MODE.txt --no-cache-dir
