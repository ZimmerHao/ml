
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
4. run server
   ```
   python manage.py runserver 0.0.0.0:8000 --settings=settings.local
   ```




## set DJANGO_SETTINGS_MODULE

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'



