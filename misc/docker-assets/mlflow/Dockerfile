FROM python:3.6.8-stretch

LABEL maintainer "Xi Wang"

RUN mkdir /mlflow/
RUN mkdir -p /mnt/mlruns/

RUN pip install mlflow==1.0.0 \
	&& pip uninstall -y cloudpickle \
	&& pip install cloudpickle==0.6.1

EXPOSE 5000

CMD cd /mnt/mlruns/ && \

