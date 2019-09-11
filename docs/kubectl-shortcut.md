####build dev image
```bash
docker build --build-arg MODE=dev --build-arg DJANGO_SETTINGS_MODULE=settings.dev -t wangxisea/dp:0.1 .

```

####install spark-livy-zeppelin
```bash
(cd k8s/spark-zeppelin-livy ; helm upgrade --install spark-tony $(pwd) --set Namespace=ns-tony)
```

##### unintall spark-livy-zepplein
(cd k8s/spark_operator ; helm delete spark-tony)