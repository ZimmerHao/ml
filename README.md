
## Run on your local

1. create db (pg)
2. install python dependency, maybe you need `virtualenv`.
   
   ```
   pip install -r requirements/common.txt
   ```
3. django migrate

   ```
   django manage.py migrate --settings=settings.local
   ```
4. init k8s resource k8s_resource_init --settings=settings.local

   ```
   django manage.py 
   ```
5. run server

   ```
   python manage.py runserver 0.0.0.0:5000 --settings=settings.local
   ```

## Run in docker (docker-compose)

1. create db (pg)
2. create .env file
   ```
   echo "DJANGO_SETTINGS_MODULE=settings.local" > .env
   ```
3. run server
    ```
    docker-compose build --build-arg MODE=prod web
    docker-compose up -d
    ```

## Run on prod (k8s)


## Attention

   * Please configure Django ALLOWED_HOSTS
   * If you run on mac, please configure shared path
   * Don't forget to create `logs` dir when run local






