#!/usr/bin/env bash

kubectl apply -f manifest/spark-operator-crds.yaml
kubectl apply -f manifest/spark-operator-rbac.yaml
kubectl apply -f manifest/spark-rbac.yaml
kubectl apply -f manifest/spark-operator.yaml