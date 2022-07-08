#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input

ls data | xargs -I {} bash -c "python3 manage.py loaddata data/{}"

exec "$@"