#news


## set DJANGO_SETTINGS_MODULE

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'


## pg

`SELECT * FROM geo_name_raw WHERE country_code = 'MY' AND alternate_names @> ARRAY['马六甲'] :: varchar[]`

`/usr/local/postgresql-9.5.4/bin/pg_dump --host 192.168.90.10 --port 5432 --username postgres --format plain --verbose --file "/home/vagrant/google.dump" --table geo_google_geo_code goparcel`

`pg_restore -U <username> -d <dbname> -1 <filename>.dump`

